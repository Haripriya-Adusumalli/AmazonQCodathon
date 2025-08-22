import boto3
import json

def add_action_groups_to_agent():
    """Add action groups to the Bedrock agent to use Lambda functions"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'
    
    # Get Lambda function ARNs
    functions = {
        'market-demand-agent': lambda_client.get_function(FunctionName='market-demand-agent')['Configuration']['FunctionArn'],
        'competitor-scan-agent': lambda_client.get_function(FunctionName='competitor-scan-agent')['Configuration']['FunctionArn'],
        'capability-match-agent': lambda_client.get_function(FunctionName='capability-match-agent')['Configuration']['FunctionArn']
    }
    
    # API Schema for action groups
    api_schema = {
        "openapi": "3.0.0",
        "info": {"title": "Product Opportunity Analysis API", "version": "1.0.0"},
        "paths": {
            "/analyze-demand": {
                "post": {
                    "description": "Analyze market demand for a product",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string", "description": "Product to analyze"},
                                        "region": {"type": "string", "description": "Geographic region"}
                                    },
                                    "required": ["query"]
                                }
                            }
                        }
                    }
                }
            },
            "/analyze-competition": {
                "post": {
                    "description": "Analyze market competition for a product",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string", "description": "Product to analyze"},
                                        "category": {"type": "string", "description": "Product category"}
                                    },
                                    "required": ["query"]
                                }
                            }
                        }
                    }
                }
            },
            "/analyze-capability": {
                "post": {
                    "description": "Analyze internal capability to build a product",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string", "description": "Product to analyze"},
                                        "required_skills": {"type": "array", "items": {"type": "string"}}
                                    },
                                    "required": ["query"]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    # Add action groups
    action_groups = [
        {
            'name': 'market-demand-analysis',
            'description': 'Analyze market demand and trends',
            'lambda_arn': functions['market-demand-agent']
        },
        {
            'name': 'competition-analysis', 
            'description': 'Analyze competitive landscape',
            'lambda_arn': functions['competitor-scan-agent']
        },
        {
            'name': 'capability-analysis',
            'description': 'Analyze internal capabilities',
            'lambda_arn': functions['capability-match-agent']
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
                    'payload': json.dumps(api_schema)
                }
            )
            print(f"Added action group: {action_group['name']}")
            
        except Exception as e:
            print(f"Error adding {action_group['name']}: {e}")
    
    # Prepare agent with new action groups
    try:
        bedrock.prepare_agent(agentId=agent_id)
        print("Agent prepared with action groups")
        
        # Update alias
        aliases = bedrock.list_agent_aliases(agentId=agent_id)
        if aliases['agentAliasSummaries']:
            alias_id = aliases['agentAliasSummaries'][0]['agentAliasId']
            bedrock.update_agent_alias(
                agentId=agent_id,
                agentAliasId=alias_id,
                agentAliasName='live',
                description='Live agent with Lambda action groups'
            )
            print(f"Updated alias: {alias_id}")
            
    except Exception as e:
        print(f"Error preparing agent: {e}")

if __name__ == "__main__":
    add_action_groups_to_agent()