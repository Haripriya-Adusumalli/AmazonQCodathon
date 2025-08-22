import boto3
import json
import time
import zipfile
import os

def deploy_full_system():
    """Deploy complete product opportunity system with Lambda functions and DynamoDB"""
    
    print("Deploying complete product opportunity system...")
    
    # Deploy Lambda functions
    lambda_functions = deploy_lambda_functions()
    
    # Create DynamoDB table
    create_dynamodb_table()
    
    # Update agent with action groups
    update_agent_with_actions(lambda_functions)
    
    print("Full system deployment complete!")

def deploy_lambda_functions():
    """Deploy all Lambda functions"""
    
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
    
    permissions_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream", 
                "logs:PutLogEvents",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Query",
                "dynamodb:Scan"
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
            PolicyName='ProductOpportunityLambdaPolicy',
            PolicyDocument=json.dumps(permissions_policy)
        )
        
        print("Created Lambda execution role")
        
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
        print("Using existing Lambda role")
    
    time.sleep(10)
    
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
                try:
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
                    
                    print(f"Created {config['name']}")
                    
                except lambda_client.exceptions.ResourceConflictException:
                    # Function already exists, get its ARN
                    response = lambda_client.get_function(FunctionName=config['name'])
                    functions[config['name']] = {
                        'arn': response['Configuration']['FunctionArn'],
                        'name': response['Configuration']['FunctionName']
                    }
                    print(f"Using existing {config['name']}")
                    
        except Exception as e:
            print(f"Error deploying {config['name']}: {e}")
    
    return functions

def create_lambda_package(function_file):
    """Create deployment package for Lambda function"""
    
    zip_path = f"lambda/{function_file.replace('.py', '')}.zip"
    
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        zip_file.write(f"lambda/{function_file}", function_file)
    
    return zip_path

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
        print("Created DynamoDB table: ProductOpportunityAnalysis")
        
    except dynamodb.exceptions.ResourceInUseException:
        print("DynamoDB table already exists")

def update_agent_with_actions(lambda_functions):
    """Update the Bedrock agent with action groups"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = 'DKPL7RP9OU'
    
    # Create action group schema
    action_group_schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "Product Opportunity Analysis API",
            "version": "1.0.0"
        },
        "paths": {
            "/analyze-demand": {
                "post": {
                    "description": "Analyze market demand for a product",
                    "parameters": [
                        {
                            "name": "query",
                            "in": "query",
                            "description": "Product or market to analyze",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Demand analysis results",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "demand_score": {"type": "number"},
                                            "trending_topics": {"type": "array"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    try:
        # Add action group to agent
        if 'market-demand-agent' in lambda_functions:
            bedrock.create_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupName='market-analysis',
                description='Market demand analysis actions',
                actionGroupExecutor={
                    'lambda': lambda_functions['market-demand-agent']['arn']
                },
                apiSchema={
                    'payload': json.dumps(action_group_schema)
                }
            )
            print("Added market analysis action group")
            
        # Prepare agent with new actions
        bedrock.prepare_agent(agentId=agent_id)
        print("Updated agent with action groups")
        
    except Exception as e:
        print(f"Error updating agent: {e}")

if __name__ == "__main__":
    deploy_full_system()