import boto3
import json

def fix_approval_issue():
    """Fix the approval prompt issue by updating action groups"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'  # Your agent ID
    
    print("Fixing approval prompt issue...")
    
    # First, remove existing action groups
    try:
        action_groups = bedrock.list_agent_action_groups(
            agentId=agent_id,
            agentVersion='DRAFT'
        )
        
        for ag in action_groups.get('actionGroupSummaries', []):
            bedrock.delete_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupId=ag['actionGroupId']
            )
            print(f"Removed action group: {ag['actionGroupName']}")
            
    except Exception as e:
        print(f"Error removing action groups: {e}")
    
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
    
    # Create action groups with function definitions (no OpenAPI)
    action_groups = [
        {
            'name': 'market-demand-analysis',
            'description': 'Analyze market demand and trends for products',
            'lambda_arn': functions['market-demand-agent'],
            'functions': [
                {
                    'name': 'analyze_market_demand',
                    'description': 'Analyze market demand for a specific product',
                    'parameters': {
                        'query': {
                            'description': 'Product name or description to analyze',
                            'type': 'string',
                            'required': True
                        },
                        'region': {
                            'description': 'Geographic region for analysis (default: US)',
                            'type': 'string',
                            'required': False
                        }
                    }
                }
            ]
        },
        {
            'name': 'competition-analysis',
            'description': 'Analyze competitive landscape for products',
            'lambda_arn': functions['competitor-scan-agent'],
            'functions': [
                {
                    'name': 'analyze_competition',
                    'description': 'Analyze competition level for a specific product',
                    'parameters': {
                        'query': {
                            'description': 'Product name or description to analyze',
                            'type': 'string',
                            'required': True
                        },
                        'category': {
                            'description': 'Product category for focused analysis',
                            'type': 'string',
                            'required': False
                        }
                    }
                }
            ]
        },
        {
            'name': 'capability-analysis',
            'description': 'Analyze internal capability to develop products',
            'lambda_arn': functions['capability-match-agent'],
            'functions': [
                {
                    'name': 'analyze_capability',
                    'description': 'Analyze capability to build a specific product',
                    'parameters': {
                        'query': {
                            'description': 'Product name or description to analyze',
                            'type': 'string',
                            'required': True
                        },
                        'required_skills': {
                            'description': 'List of required skills for the product',
                            'type': 'array',
                            'required': False
                        }
                    }
                }
            ]
        }
    ]
    
    # Create new action groups with function definitions
    for action_group in action_groups:
        try:
            # Build function schema
            function_schema = {
                'functions': []
            }
            
            for func in action_group['functions']:
                function_def = {
                    'name': func['name'],
                    'description': func['description'],
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': []
                    }
                }
                
                for param_name, param_info in func['parameters'].items():
                    function_def['parameters']['properties'][param_name] = {
                        'type': param_info['type'],
                        'description': param_info['description']
                    }
                    if param_info['required']:
                        function_def['parameters']['required'].append(param_name)
                
                function_schema['functions'].append(function_def)
            
            response = bedrock.create_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupName=action_group['name'],
                description=action_group['description'],
                actionGroupExecutor={
                    'lambda': action_group['lambda_arn']
                },
                functionSchema={
                    'functions': function_schema['functions']
                },
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
        
        # Update alias
        aliases = bedrock.list_agent_aliases(agentId=agent_id)
        if aliases['agentAliasSummaries']:
            alias_id = aliases['agentAliasSummaries'][0]['agentAliasId']
            bedrock.update_agent_alias(
                agentId=agent_id,
                agentAliasId=alias_id,
                agentAliasName='live',
                description='Live agent without approval prompts'
            )
            print(f"Updated alias: {alias_id}")
            
    except Exception as e:
        print(f"Error preparing agent: {e}")
    
    print("\nApproval issue should now be fixed!")
    print("The agent will execute functions without asking for approval.")

if __name__ == "__main__":
    fix_approval_issue()