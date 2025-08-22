import boto3
import json

def update_enhanced_agent():
    """Update enhanced agent to use new Lambda functions"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'BKWEM7GZQX'  # Enhanced agent ID
    
    # Get new Lambda function ARNs
    try:
        functions = {
            'demand': lambda_client.get_function(FunctionName='enhanced-market-demand-copy')['Configuration']['FunctionArn'],
            'competition': lambda_client.get_function(FunctionName='enhanced-competitor-scan-copy')['Configuration']['FunctionArn'],
            'capability': lambda_client.get_function(FunctionName='enhanced-capability-match-copy')['Configuration']['FunctionArn']
        }
        print("Got enhanced function ARNs")
        
    except Exception as e:
        print(f"Error getting function ARNs: {e}")
        return
    
    # Create action groups for enhanced agent
    action_groups = [
        {
            'name': 'enhanced-demand-analysis',
            'description': 'Enhanced market demand analysis with real APIs',
            'lambda_arn': functions['demand']
        },
        {
            'name': 'enhanced-competition-analysis',
            'description': 'Enhanced competition analysis with real APIs',
            'lambda_arn': functions['competition']
        },
        {
            'name': 'enhanced-capability-analysis',
            'description': 'Enhanced capability analysis with Q Business',
            'lambda_arn': functions['capability']
        }
    ]
    
    # Create action groups
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
    try:
        print("Preparing enhanced agent...")
        bedrock.prepare_agent(agentId=agent_id)
        print("Enhanced agent prepared successfully!")
        
    except Exception as e:
        print(f"Error preparing agent: {e}")

if __name__ == "__main__":
    update_enhanced_agent()