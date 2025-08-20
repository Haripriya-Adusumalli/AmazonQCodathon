import boto3
import json
import zipfile
import os
from botocore.exceptions import NoCredentialsError, ClientError

def create_bedrock_agent():
    # Verify AWS credentials
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"Connected to AWS as: {identity['Arn']}")
    except NoCredentialsError:
        print("ERROR: AWS credentials not configured. Run 'aws configure' first.")
        return
    except Exception as e:
        print(f"ERROR: Failed to connect to AWS: {e}")
        return
    bedrock = boto3.client('bedrock-agent')
    lambda_client = boto3.client('lambda')
    iam = boto3.client('iam')
    
    # Create IAM role for Lambda
    lambda_trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        lambda_role_response = iam.create_role(
            RoleName='WeatherLambdaRole',
            AssumeRolePolicyDocument=json.dumps(lambda_trust_policy),
            Description='Role for Weather Lambda Function'
        )
        lambda_role_arn = lambda_role_response['Role']['Arn']
        
        # Attach basic Lambda execution policy
        iam.attach_role_policy(
            RoleName='WeatherLambdaRole',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
    except iam.exceptions.EntityAlreadyExistsException:
        lambda_role_arn = iam.get_role(RoleName='WeatherLambdaRole')['Role']['Arn']
    
    # Create IAM role for Bedrock agent
    bedrock_trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "bedrock.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        bedrock_role_response = iam.create_role(
            RoleName='BedrockWeatherAgentRole',
            AssumeRolePolicyDocument=json.dumps(bedrock_trust_policy),
            Description='Role for Bedrock Weather Agent'
        )
        bedrock_role_arn = bedrock_role_response['Role']['Arn']
        
        # Create and attach policy for Bedrock agent
        bedrock_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "bedrock:InvokeModel",
                        "lambda:InvokeFunction"
                    ],
                    "Resource": "*"
                }
            ]
        }
        
        iam.put_role_policy(
            RoleName='BedrockWeatherAgentRole',
            PolicyName='BedrockAgentPolicy',
            PolicyDocument=json.dumps(bedrock_policy)
        )
    except iam.exceptions.EntityAlreadyExistsException:
        bedrock_role_arn = iam.get_role(RoleName='BedrockWeatherAgentRole')['Role']['Arn']
    
    # Wait for role to be available
    import time
    time.sleep(10)
    
    # Create Lambda function
    try:
        with zipfile.ZipFile('weather-function.zip', 'w') as zip_file:
            zip_file.write('lambda/weather-function.py', 'lambda_function.py')
        
        with open('weather-function.zip', 'rb') as zip_file:
            lambda_response = lambda_client.create_function(
                FunctionName='weather-agent-function',
                Runtime='python3.9',
                Role=lambda_role_arn,
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': zip_file.read()},
                Environment={'Variables': {'WEATHER_API_KEY': os.environ.get('WEATHER_API_KEY', 'demo_key')}}
            )
    except lambda_client.exceptions.ResourceConflictException:
        lambda_response = lambda_client.get_function(FunctionName='weather-agent-function')
    
    # Clean up zip file
    if os.path.exists('weather-function.zip'):
        os.remove('weather-function.zip')
    
    # Create Bedrock agent
    with open('agent-schema.json', 'r') as f:
        api_schema = json.load(f)
    
    agent_response = bedrock.create_agent(
        agentName='weather-agent',
        description='Agent that provides current weather information for cities',
        foundationModel='anthropic.claude-3-sonnet-20240229-v1:0',
        instruction='You are a helpful weather assistant. When users ask about weather in a city, use the getCurrentWeather function to get real-time weather data.',
        agentResourceRoleArn=bedrock_role_arn
    )
    
    agent_id = agent_response['agent']['agentId']
    
    # Create action group
    bedrock.create_agent_action_group(
        agentId=agent_id,
        agentVersion='DRAFT',
        actionGroupName='weather-actions',
        description='Actions for getting weather data',
        actionGroupExecutor={
            'lambda': lambda_response['FunctionArn']
        },
        apiSchema={
            'payload': json.dumps(api_schema)
        }
    )
    
    print(f"Bedrock agent created with ID: {agent_id}")
    return agent_id

if __name__ == "__main__":
    create_bedrock_agent()