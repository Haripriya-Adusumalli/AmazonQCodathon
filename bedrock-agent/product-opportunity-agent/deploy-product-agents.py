import boto3
import json
import time
import zipfile
import os

def deploy_product_opportunity_system():
    """Deploy the complete product opportunity recommendation system"""
    
    print("🚀 Deploying Product Opportunity System...")
    
    # Deploy Lambda functions
    lambda_functions = deploy_lambda_functions()
    
    # Deploy Bedrock agents
    agents = deploy_bedrock_agents(lambda_functions)
    
    # Create DynamoDB table for storing analysis results
    create_dynamodb_table()
    
    # Save configuration
    config = {
        'lambda_functions': lambda_functions,
        'agents': agents,
        'region': 'us-east-1'
    }
    
    with open('product-opportunity-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Product Opportunity System deployed successfully!")
    return config

def deploy_lambda_functions():
    """Deploy all Lambda functions for the agents"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    iam = boto3.client('iam')
    
    # Create Lambda execution role
    role_name = 'ProductOpportunityLambdaRole'
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    try:
        role_response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        role_arn = role_response['Role']['Arn']
        
        # Attach basic execution policy
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
    
    time.sleep(10)  # Wait for role propagation
    
    functions = {}
    
    # Deploy each Lambda function
    lambda_configs = [
        {
            'name': 'market-demand-agent',
            'file': 'market-demand-function.py',
            'description': 'Analyzes market demand signals'
        },
        {
            'name': 'competitor-scan-agent', 
            'file': 'competitor-scan-function.py',
            'description': 'Scans competitive landscape'
        },
        {
            'name': 'capability-match-agent',
            'file': 'capability-match-function.py', 
            'description': 'Matches internal capabilities'
        }
    ]
    
    for config in lambda_configs:
        try:
            # Create deployment package
            zip_path = create_lambda_package(config['file'])
            
            with open(zip_path, 'rb') as zip_file:
                response = lambda_client.create_function(
                    FunctionName=config['name'],
                    Runtime='python3.9',
                    Role=role_arn,
                    Handler=f"{config['file'].replace('.py', '')}.lambda_handler",
                    Code={'ZipFile': zip_file.read()},
                    Description=config['description'],
                    Timeout=30
                )
                
                functions[config['name']] = {
                    'arn': response['FunctionArn'],
                    'name': response['FunctionName']
                }
                
                print(f"✅ Deployed {config['name']}")
                
        except lambda_client.exceptions.ResourceConflictException:
            # Function already exists, get its ARN
            response = lambda_client.get_function(FunctionName=config['name'])
            functions[config['name']] = {
                'arn': response['Configuration']['FunctionArn'],
                'name': response['Configuration']['FunctionName']
            }
            print(f"✅ Using existing {config['name']}")
    
    return functions

def create_lambda_package(function_file):
    """Create deployment package for Lambda function"""
    
    zip_path = f"lambda/{function_file.replace('.py', '')}.zip"
    
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        zip_file.write(f"lambda/{function_file}", function_file)
    
    return zip_path

def deploy_bedrock_agents(lambda_functions):
    """Deploy Bedrock agents with Lambda integrations"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    iam = boto3.client('iam')
    
    # Create agent role
    role_name = 'ProductOpportunityAgentRole'
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "bedrock.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    permissions_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "lambda:InvokeFunction",
                "dynamodb:*"
            ],
            "Resource": "*"
        }]
    }
    
    try:
        role_response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        role_arn = role_response['Role']['Arn']
        
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName='ProductOpportunityAgentPolicy',
            PolicyDocument=json.dumps(permissions_policy)
        )
        
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
    
    time.sleep(10)
    
    # Create main orchestrator agent
    agent_instruction = """
    You are a Product Opportunity Orchestrator that identifies high-potential product opportunities.
    
    Analyze user queries about product ideas and calculate DCC scores:
    - Demand: Market interest and momentum
    - Competition: Current market saturation  
    - Capability: Internal readiness to execute
    
    Provide ranked recommendations with specific differentiation strategies and next steps.
    """
    
    try:
        agent_response = bedrock.create_agent(
            agentName='product-opportunity-orchestrator',
            description='Orchestrates product opportunity analysis',
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
            instruction=agent_instruction,
            agentResourceRoleArn=role_arn
        )
        
        agent_id = agent_response['agent']['agentId']
        
        # Prepare and create alias
        bedrock.prepare_agent(agentId=agent_id)
        time.sleep(30)
        
        alias_response = bedrock.create_agent_alias(
            agentId=agent_id,
            agentAliasName='live'
        )
        
        alias_id = alias_response['agentAlias']['agentAliasId']
        
        print(f"✅ Created orchestrator agent: {agent_id}")
        
        return {
            'orchestrator': {
                'agentId': agent_id,
                'aliasId': alias_id
            }
        }
        
    except Exception as e:
        print(f"Error creating agent: {e}")
        return {}

def create_dynamodb_table():
    """Create DynamoDB table for storing analysis results"""
    
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    
    try:
        dynamodb.create_table(
            TableName='ProductOpportunityAnalysis',
            KeySchema=[
                {'AttributeName': 'query_id', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'query_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("✅ Created DynamoDB table")
        
    except dynamodb.exceptions.ResourceInUseException:
        print("✅ DynamoDB table already exists")

if __name__ == "__main__":
    deploy_product_opportunity_system()