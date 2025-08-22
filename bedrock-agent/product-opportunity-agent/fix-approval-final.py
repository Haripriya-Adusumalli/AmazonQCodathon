import boto3
import json

def fix_approval_final():
    """Fix approval issue with correct function schema format"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'
    
    print("Fixing approval issue with correct schema...")
    
    # First disable existing action groups
    try:
        action_groups = bedrock.list_agent_action_groups(
            agentId=agent_id,
            agentVersion='DRAFT'
        )
        
        for ag in action_groups.get('actionGroupSummaries', []):
            try:
                bedrock.update_agent_action_group(
                    agentId=agent_id,
                    agentVersion='DRAFT',
                    actionGroupId=ag['actionGroupId'],
                    actionGroupName=ag['actionGroupName'],
                    actionGroupState='DISABLED'
                )
                print(f"Disabled action group: {ag['actionGroupName']}")
            except Exception as e:
                print(f"Error disabling {ag['actionGroupName']}: {e}")
                
    except Exception as e:
        print(f"Error listing action groups: {e}")
    
    # Get Lambda function ARNs
    try:
        functions = {
            'market-demand-agent': lambda_client.get_function(FunctionName='market-demand-agent')['Configuration']['FunctionArn'],
            'competitor-scan-agent': lambda_client.get_function(FunctionName='competitor-scan-agent')['Configuration']['FunctionArn'],
            'capability-match-agent': lambda_client.get_function(FunctionName='capability-match-agent')['Configuration']['FunctionArn']
        }
    except Exception as e:
        print(f"Error getting Lambda functions: {e}")
        return
    
    # Create action groups with simplified function schema
    action_groups = [
        {
            'name': 'market-demand-simple',
            'description': 'Analyze market demand for products',
            'lambda_arn': functions['market-demand-agent'],
            'function': {
                'name': 'analyze_demand',
                'description': 'Get market demand analysis for a product',
                'parameters': {
                    'query': {
                        'description': 'Product to analyze',
                        'type': 'string',
                        'required': True
                    }
                }
            }
        },
        {
            'name': 'competition-simple',
            'description': 'Analyze competition for products',
            'lambda_arn': functions['competitor-scan-agent'],
            'function': {
                'name': 'analyze_competition',
                'description': 'Get competition analysis for a product',
                'parameters': {
                    'query': {
                        'description': 'Product to analyze',
                        'type': 'string',
                        'required': True
                    }
                }
            }
        },
        {
            'name': 'capability-simple',
            'description': 'Analyze capability to build products',
            'lambda_arn': functions['capability-match-agent'],
            'function': {
                'name': 'analyze_capability',
                'description': 'Get capability analysis for a product',
                'parameters': {
                    'query': {
                        'description': 'Product to analyze',
                        'type': 'string',
                        'required': True
                    }
                }
            }
        }
    ]
    
    # Create new action groups
    for action_group in action_groups:
        try:
            # Build proper function schema
            func = action_group['function']
            properties = {}
            required = []
            
            for param_name, param_info in func['parameters'].items():
                properties[param_name] = {
                    'type': param_info['type'],
                    'description': param_info['description']
                }
                if param_info['required']:
                    required.append(param_name)
            
            function_schema = {
                'functions': [
                    {
                        'name': func['name'],
                        'description': func['description'],
                        'parameters': {
                            'type': 'object',
                            'properties': properties,
                            'required': required
                        }
                    }
                ]
            }
            
            response = bedrock.create_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupName=action_group['name'],
                description=action_group['description'],
                actionGroupExecutor={
                    'lambda': action_group['lambda_arn']
                },
                functionSchema=function_schema,
                actionGroupState='ENABLED'
            )
            
            print(f"Created action group: {action_group['name']}")
            
        except Exception as e:
            print(f"Error creating {action_group['name']}: {e}")
    
    # Prepare agent
    try:
        print("Preparing agent...")
        bedrock.prepare_agent(agentId=agent_id)
        print("Agent prepared successfully")
        
    except Exception as e:
        print(f"Error preparing agent: {e}")
    
    print("\\nApproval issue fix completed!")
    print("Test the agent - it should now execute without approval prompts.")

if __name__ == "__main__":
    fix_approval_final()