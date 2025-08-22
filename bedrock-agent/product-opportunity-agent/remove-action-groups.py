import boto3

def remove_action_groups():
    """Remove action groups to let agent work without Lambda integration"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = 'DKPL7RP9OU'
    
    # List and delete action groups
    try:
        action_groups = bedrock.list_agent_action_groups(
            agentId=agent_id,
            agentVersion='DRAFT'
        )
        
        for ag in action_groups['actionGroupSummaries']:
            bedrock.delete_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupId=ag['actionGroupId']
            )
            print(f"Deleted action group: {ag['actionGroupName']}")
        
        # Prepare agent without action groups
        bedrock.prepare_agent(agentId=agent_id)
        print("Agent prepared without action groups")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    remove_action_groups()