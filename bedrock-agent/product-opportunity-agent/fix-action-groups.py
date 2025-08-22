import boto3
import json

def fix_action_groups():
    """Fix action groups with correct API schema"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'
    
    # Get Lambda ARNs
    market_arn = lambda_client.get_function(FunctionName='market-demand-agent')['Configuration']['FunctionArn']
    competitor_arn = lambda_client.get_function(FunctionName='competitor-scan-agent')['Configuration']['FunctionArn']
    capability_arn = lambda_client.get_function(FunctionName='capability-match-agent')['Configuration']['FunctionArn']
    
    # Simple API schemas for each function
    market_schema = {
        "openapi": "3.0.0",
        "info": {"title": "Market Demand API", "version": "1.0.0"},
        "paths": {
            "/analyze-demand": {
                "post": {
                    "description": "Analyze market demand for a product",
                    "parameters": [
                        {
                            "name": "query",
                            "in": "query", 
                            "description": "Product to analyze",
                            "required": True,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "region",
                            "in": "query",
                            "description": "Geographic region", 
                            "required": False,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Demand analysis results"
                        }
                    }
                }
            }
        }
    }
    
    competitor_schema = {
        "openapi": "3.0.0", 
        "info": {"title": "Competition API", "version": "1.0.0"},
        "paths": {
            "/analyze-competition": {
                "post": {
                    "description": "Analyze market competition",
                    "parameters": [
                        {
                            "name": "query",
                            "in": "query",
                            "description": "Product to analyze", 
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Competition analysis results"
                        }
                    }
                }
            }
        }
    }
    
    capability_schema = {
        "openapi": "3.0.0",
        "info": {"title": "Capability API", "version": "1.0.0"},
        "paths": {
            "/analyze-capability": {
                "post": {
                    "description": "Analyze internal capabilities",
                    "parameters": [
                        {
                            "name": "query", 
                            "in": "query",
                            "description": "Product to analyze",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Capability analysis results"
                        }
                    }
                }
            }
        }
    }
    
    # Create action groups
    action_groups = [
        {
            'name': 'market-demand',
            'description': 'Analyze market demand and trends',
            'lambda_arn': market_arn,
            'schema': market_schema
        },
        {
            'name': 'competition-scan',
            'description': 'Analyze competitive landscape', 
            'lambda_arn': competitor_arn,
            'schema': competitor_schema
        },
        {
            'name': 'capability-match',
            'description': 'Analyze internal capabilities',
            'lambda_arn': capability_arn,
            'schema': capability_schema
        }
    ]
    
    for action_group in action_groups:
        try:
            response = bedrock.create_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupName=action_group['name'],
                description=action_group['description'],
                actionGroupExecutor={
                    'lambda': action_group['lambda_arn']
                },
                apiSchema={
                    'payload': json.dumps(action_group['schema'])
                }
            )
            print(f"Created action group: {action_group['name']}")
            
        except Exception as e:
            print(f"Error creating {action_group['name']}: {e}")
    
    # Prepare agent
    try:
        bedrock.prepare_agent(agentId=agent_id)
        print("Agent prepared with action groups")
    except Exception as e:
        print(f"Error preparing agent: {e}")

if __name__ == "__main__":
    fix_action_groups()