import boto3

def add_separate_action_groups():
    """Add separate action groups for each enhanced Lambda function"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'BKWEM7GZQX'
    
    # Get Lambda ARNs
    functions = {
        'demand': lambda_client.get_function(FunctionName='enhanced-market-demand-copy')['Configuration']['FunctionArn'],
        'competition': lambda_client.get_function(FunctionName='enhanced-competitor-scan-copy')['Configuration']['FunctionArn'],
        'capability': lambda_client.get_function(FunctionName='enhanced-capability-match-copy')['Configuration']['FunctionArn']
    }
    
    # Remove existing action group
    try:
        existing_groups = bedrock.list_agent_action_groups(
            agentId=agent_id,
            agentVersion='DRAFT'
        )
        
        for group in existing_groups.get('actionGroupSummaries', []):
            bedrock.delete_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupId=group['actionGroupId']
            )
            print(f"Deleted: {group['actionGroupName']}")
            
    except Exception as e:
        print(f"Cleanup error: {e}")
    
    # Create separate action groups
    action_groups = [
        {
            'name': 'demand-analysis',
            'description': 'Analyze market demand',
            'lambda_arn': functions['demand'],
            'function': {
                'name': 'analyze_market_demand',
                'description': 'Analyze market demand for a product',
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
            'name': 'competition-analysis',
            'description': 'Analyze competition',
            'lambda_arn': functions['competition'],
            'function': {
                'name': 'analyze_competition',
                'description': 'Analyze competition for a product',
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
            'name': 'capability-analysis',
            'description': 'Analyze capabilities',
            'lambda_arn': functions['capability'],
            'function': {
                'name': 'analyze_capability',
                'description': 'Analyze capability to build a product',
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
    
    for ag in action_groups:
        try:
            function_schema = {
                'functions': [{
                    'name': ag['function']['name'],
                    'description': ag['function']['description'],
                    'parameters': ag['function']['parameters']
                }]
            }
            
            bedrock.create_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupName=ag['name'],
                description=ag['description'],
                actionGroupExecutor={'lambda': ag['lambda_arn']},
                functionSchema=function_schema,
                actionGroupState='ENABLED'
            )
            print(f"Created: {ag['name']}")
            
        except Exception as e:
            print(f"Error creating {ag['name']}: {e}")
    
    # Prepare agent
    try:
        bedrock.prepare_agent(agentId=agent_id)
        print("Enhanced agent prepared with separate action groups!")
        
    except Exception as e:
        print(f"Prepare error: {e}")

if __name__ == "__main__":
    add_separate_action_groups()