import boto3
import json
import time

def deploy_enhanced_agent():
    """Deploy enhanced product opportunity agent with proper action groups"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    iam = boto3.client('iam')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Create new IAM role for enhanced agent
    role_name = 'EnhancedProductOpportunityRole'
    
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
                "lambda:InvokeFunction"
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
            PolicyName='EnhancedProductOpportunityPolicy',
            PolicyDocument=json.dumps(permissions_policy)
        )
        print("Created IAM role")
        
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
        print("Using existing IAM role")
    
    time.sleep(10)
    
    # Enhanced agent instruction
    agent_instruction = """
You are an Enhanced Product Opportunity Analyzer that uses real market data to identify high-potential product opportunities.

When analyzing product opportunities, you MUST call all three analysis functions:

1. FIRST call analyze_market_demand to get demand analysis
2. THEN call analyze_competition to get competition analysis  
3. FINALLY call analyze_capability to get capability analysis

After getting all three analyses, calculate the DCC score:
DCC = (Demand × 0.45) + ((100 - Competition) × 0.30) + (Capability × 0.25)

Provide comprehensive recommendations based on all three analyses.
Always execute all functions automatically without asking for approval.
"""
    
    try:
        # Create enhanced agent
        agent_response = bedrock.create_agent(
            agentName='enhanced-product-opportunity-analyzer',
            description='Enhanced product opportunity analyzer with real API integration',
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
            instruction=agent_instruction,
            agentResourceRoleArn=role_arn
        )
        
        agent_id = agent_response['agent']['agentId']
        print(f"Created enhanced agent: {agent_id}")
        
        # Get Lambda function ARNs
        functions = {
            'market-demand': lambda_client.get_function(FunctionName='market-demand-agent')['Configuration']['FunctionArn'],
            'competitor-scan': lambda_client.get_function(FunctionName='competitor-scan-agent')['Configuration']['FunctionArn'],
            'capability-match': lambda_client.get_function(FunctionName='capability-match-agent')['Configuration']['FunctionArn']
        }
        
        # Create action groups for each function
        action_groups = [
            {
                'name': 'demand-analysis',
                'description': 'Analyze market demand using real trend data',
                'lambda_arn': functions['market-demand'],
                'function': {
                    'name': 'analyze_market_demand',
                    'description': 'Get market demand analysis for a product',
                    'parameters': {
                        'query': {'type': 'string', 'description': 'Product to analyze', 'required': True},
                        'region': {'type': 'string', 'description': 'Geographic region', 'required': False}
                    }
                }
            },
            {
                'name': 'competition-analysis',
                'description': 'Analyze competition using real market data',
                'lambda_arn': functions['competitor-scan'],
                'function': {
                    'name': 'analyze_competition',
                    'description': 'Get competition analysis for a product',
                    'parameters': {
                        'query': {'type': 'string', 'description': 'Product to analyze', 'required': True},
                        'category': {'type': 'string', 'description': 'Product category', 'required': False}
                    }
                }
            },
            {
                'name': 'capability-analysis',
                'description': 'Analyze internal capability to build products',
                'lambda_arn': functions['capability-match'],
                'function': {
                    'name': 'analyze_capability',
                    'description': 'Get capability analysis for a product',
                    'parameters': {
                        'query': {'type': 'string', 'description': 'Product to analyze', 'required': True}
                    }
                }
            }
        ]
        
        # Create action groups
        for ag in action_groups:
            func = ag['function']
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
                'functions': [{
                    'name': func['name'],
                    'description': func['description'],
                    'parameters': {
                        'type': 'object',
                        'properties': properties,
                        'required': required
                    }
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
            print(f"Created action group: {ag['name']}")
        
        # Prepare agent
        print("Preparing agent...")
        bedrock.prepare_agent(agentId=agent_id)
        time.sleep(45)
        
        # Create alias
        alias_response = bedrock.create_agent_alias(
            agentId=agent_id,
            agentAliasName='enhanced',
            description='Enhanced agent with real APIs'
        )
        alias_id = alias_response['agentAlias']['agentAliasId']
        
        # Save config
        config = {
            'agentId': agent_id,
            'aliasId': alias_id,
            'region': 'us-east-1'
        }
        
        with open('enhanced-agent-config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\\nEnhanced agent deployed successfully!")
        print(f"Agent ID: {agent_id}")
        print(f"Alias ID: {alias_id}")
        
        return config
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    deploy_enhanced_agent()