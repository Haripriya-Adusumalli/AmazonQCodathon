import boto3
import json
import time

def create_simple_enhanced_agent():
    """Create enhanced agent using existing Lambda functions"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    iam = boto3.client('iam')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Use existing role
    role_arn = iam.get_role(RoleName='ProductOpportunityAgentRole')['Role']['Arn']
    
    # Enhanced agent instruction
    agent_instruction = """
You are an Enhanced Product Opportunity Analyzer that performs comprehensive DCC analysis.

When analyzing product opportunities, you MUST:

1. Call analyze_market_demand function to get demand analysis
2. Call analyze_competition function to get competition analysis  
3. Call analyze_capability function to get capability analysis

After getting all analyses, calculate:
DCC = (Demand × 0.45) + ((100 - Competition) × 0.30) + (Capability × 0.25)

Provide detailed recommendations based on all three analyses.
Execute all functions automatically without asking for approval.
"""
    
    try:
        # Create enhanced agent
        agent_response = bedrock.create_agent(
            agentName='enhanced-product-analyzer',
            description='Enhanced product opportunity analyzer with comprehensive analysis',
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
            instruction=agent_instruction,
            agentResourceRoleArn=role_arn
        )
        
        agent_id = agent_response['agent']['agentId']
        print(f"Created enhanced agent: {agent_id}")
        
        # Get existing Lambda function ARNs
        functions = {
            'market-demand': lambda_client.get_function(FunctionName='market-demand-agent')['Configuration']['FunctionArn'],
            'competitor-scan': lambda_client.get_function(FunctionName='competitor-scan-agent')['Configuration']['FunctionArn'],
            'capability-match': lambda_client.get_function(FunctionName='capability-match-agent')['Configuration']['FunctionArn']
        }
        
        # Create simple action groups without complex schemas
        action_groups = [
            {
                'name': 'demand-analysis',
                'description': 'Analyze market demand',
                'lambda_arn': functions['market-demand']
            },
            {
                'name': 'competition-analysis',
                'description': 'Analyze competition',
                'lambda_arn': functions['competitor-scan']
            },
            {
                'name': 'capability-analysis',
                'description': 'Analyze capabilities',
                'lambda_arn': functions['capability-match']
            }
        ]
        
        # Create action groups without function schemas
        for ag in action_groups:
            try:
                bedrock.create_agent_action_group(
                    agentId=agent_id,
                    agentVersion='DRAFT',
                    actionGroupName=ag['name'],
                    description=ag['description'],
                    actionGroupExecutor={'lambda': ag['lambda_arn']},
                    actionGroupState='ENABLED'
                )
                print(f"Created action group: {ag['name']}")
                
            except Exception as e:
                print(f"Error creating {ag['name']}: {e}")
        
        # Prepare agent
        print("Preparing agent...")
        bedrock.prepare_agent(agentId=agent_id)
        time.sleep(45)
        
        # Create alias
        alias_response = bedrock.create_agent_alias(
            agentId=agent_id,
            agentAliasName='enhanced',
            description='Enhanced agent with all functions'
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
        
        print(f"\\nEnhanced agent created successfully!")
        print(f"Agent ID: {agent_id}")
        print(f"Alias ID: {alias_id}")
        print("\\nUpdate your React app to use this enhanced agent.")
        
        return config
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    create_simple_enhanced_agent()