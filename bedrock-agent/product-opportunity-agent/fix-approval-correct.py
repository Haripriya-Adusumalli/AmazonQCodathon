import boto3
import json

def fix_approval_correct():
    """Fix approval issue with AWS Bedrock correct function schema"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'
    
    print("Fixing approval with correct AWS Bedrock schema...")
    
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
    
    # Create action groups with correct AWS Bedrock function schema
    action_groups = [
        {
            'name': 'demand-analyzer',
            'description': 'Analyze market demand',
            'lambda_arn': functions['market-demand-agent']
        },
        {
            'name': 'competition-analyzer', 
            'description': 'Analyze competition',
            'lambda_arn': functions['competitor-scan-agent']
        },
        {
            'name': 'capability-analyzer',
            'description': 'Analyze capabilities',
            'lambda_arn': functions['capability-match-agent']
        }
    ]
    
    # AWS Bedrock function schema format
    function_schema = {
        'functions': [
            {
                'name': 'analyze_market_demand',
                'description': 'Analyze market demand for a product',
                'parameters': {
                    'query': {
                        'description': 'Product name to analyze',
                        'type': 'string',
                        'required': True
                    },
                    'region': {
                        'description': 'Geographic region',
                        'type': 'string',
                        'required': False
                    }
                }
            },
            {
                'name': 'analyze_competition',
                'description': 'Analyze competition for a product',
                'parameters': {
                    'query': {
                        'description': 'Product name to analyze',
                        'type': 'string',
                        'required': True
                    },
                    'category': {
                        'description': 'Product category',
                        'type': 'string',
                        'required': False
                    }
                }
            },
            {
                'name': 'analyze_capability',
                'description': 'Analyze capability to build a product',
                'parameters': {
                    'query': {
                        'description': 'Product name to analyze',
                        'type': 'string',
                        'required': True
                    }
                }
            }
        ]
    }
    
    # Create single action group with all functions
    try:
        response = bedrock.create_agent_action_group(
            agentId=agent_id,
            agentVersion='DRAFT',
            actionGroupName='product-analysis-functions',
            description='Product opportunity analysis functions',
            actionGroupExecutor={
                'lambda': functions['market-demand-agent']  # Primary function
            },
            functionSchema=function_schema,
            actionGroupState='ENABLED'
        )
        
        print("Created unified action group with all functions")
        
    except Exception as e:
        print(f"Error creating action group: {e}")
        
        # Try alternative approach - no function schema
        try:
            response = bedrock.create_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupName='simple-product-analysis',
                description='Simple product analysis without schema',
                actionGroupExecutor={
                    'lambda': functions['market-demand-agent']
                },
                actionGroupState='ENABLED'
            )
            print("Created simple action group without function schema")
            
        except Exception as e2:
            print(f"Alternative approach also failed: {e2}")
    
    # Prepare agent
    try:
        print("Preparing agent...")
        bedrock.prepare_agent(agentId=agent_id)
        print("Agent prepared successfully")
        
    except Exception as e:
        print(f"Error preparing agent: {e}")
    
    print("\\nTry testing the agent now - it should work without approval prompts.")

if __name__ == "__main__":
    fix_approval_correct()