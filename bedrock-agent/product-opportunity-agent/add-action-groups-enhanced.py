import boto3
import json

def add_action_groups_enhanced():
    """Add action groups to enhanced agent"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'BKWEM7GZQX'  # Enhanced agent ID
    
    # Get enhanced Lambda function ARNs
    functions = {
        'demand': lambda_client.get_function(FunctionName='enhanced-market-demand-copy')['Configuration']['FunctionArn'],
        'competition': lambda_client.get_function(FunctionName='enhanced-competitor-scan-copy')['Configuration']['FunctionArn'],
        'capability': lambda_client.get_function(FunctionName='enhanced-capability-match-copy')['Configuration']['FunctionArn']
    }
    
    # Simple OpenAPI schema
    api_schema = {
        "openapi": "3.0.0",
        "info": {"title": "Enhanced Product Analysis API", "version": "1.0.0"},
        "paths": {
            "/analyze-demand": {
                "post": {
                    "description": "Analyze market demand",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/analyze-competition": {
                "post": {
                    "description": "Analyze competition",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/analyze-capability": {
                "post": {
                    "description": "Analyze capability",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    # Create action groups
    action_groups = [
        {
            'name': 'enhanced-demand',
            'description': 'Enhanced market demand analysis',
            'lambda_arn': functions['demand']
        },
        {
            'name': 'enhanced-competition',
            'description': 'Enhanced competition analysis',
            'lambda_arn': functions['competition']
        },
        {
            'name': 'enhanced-capability',
            'description': 'Enhanced capability analysis',
            'lambda_arn': functions['capability']
        }
    ]
    
    for ag in action_groups:
        try:
            bedrock.create_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupName=ag['name'],
                description=ag['description'],
                actionGroupExecutor={'lambda': ag['lambda_arn']},
                apiSchema={'payload': json.dumps(api_schema)},
                actionGroupState='ENABLED'
            )
            print(f"Created action group: {ag['name']}")
            
        except Exception as e:
            print(f"Error creating {ag['name']}: {e}")
    
    # Prepare agent
    try:
        print("Preparing enhanced agent...")
        bedrock.prepare_agent(agentId=agent_id)
        print("Enhanced agent prepared with action groups!")
        
    except Exception as e:
        print(f"Error preparing agent: {e}")

if __name__ == "__main__":
    add_action_groups_enhanced()