import boto3

def add_simple_action_groups():
    """Add simple action groups without schemas"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'BKWEM7GZQX'
    
    # Get Lambda ARNs
    functions = {
        'demand': lambda_client.get_function(FunctionName='enhanced-market-demand-copy')['Configuration']['FunctionArn'],
        'competition': lambda_client.get_function(FunctionName='enhanced-competitor-scan-copy')['Configuration']['FunctionArn'],
        'capability': lambda_client.get_function(FunctionName='enhanced-capability-match-copy')['Configuration']['FunctionArn']
    }
    
    # Remove existing action groups first
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
            print(f"Deleted existing group: {group['actionGroupName']}")
            
    except Exception as e:
        print(f"Error cleaning up: {e}")
    
    # Create new action groups with parent group approach
    try:
        bedrock.create_agent_action_group(
            agentId=agent_id,
            agentVersion='DRAFT',
            actionGroupName='enhanced-analysis-functions',
            description='Enhanced product analysis with demand, competition, and capability functions',
            actionGroupExecutor={'lambda': functions['demand']},
            actionGroupState='ENABLED'
        )
        print("Created unified action group")
        
        # Prepare agent
        bedrock.prepare_agent(agentId=agent_id)
        print("Enhanced agent prepared successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_simple_action_groups()