import boto3

def add_function_action_groups():
    """Add action groups using function schema like the working agent"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'BKWEM7GZQX'
    
    # Get Lambda ARNs
    functions = {
        'demand': lambda_client.get_function(FunctionName='enhanced-market-demand-copy')['Configuration']['FunctionArn'],
        'competition': lambda_client.get_function(FunctionName='enhanced-competitor-scan-copy')['Configuration']['FunctionArn'],
        'capability': lambda_client.get_function(FunctionName='enhanced-capability-match-copy')['Configuration']['FunctionArn']
    }
    
    # Function schema format (same as working agent)
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
        bedrock.create_agent_action_group(
            agentId=agent_id,
            agentVersion='DRAFT',
            actionGroupName='enhanced-product-analysis',
            description='Enhanced product analysis functions',
            actionGroupExecutor={'lambda': functions['demand']},
            functionSchema=function_schema,
            actionGroupState='ENABLED'
        )
        print("Created enhanced action group with function schema")
        
        # Prepare agent
        bedrock.prepare_agent(agentId=agent_id)
        print("Enhanced agent prepared successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_function_action_groups()