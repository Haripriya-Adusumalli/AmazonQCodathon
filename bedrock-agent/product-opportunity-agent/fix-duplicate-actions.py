import boto3

def fix_duplicate_actions():
    """Fix duplicate action groups by disabling and deleting"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = 'DKPL7RP9OU'
    
    try:
        action_groups = bedrock.list_agent_action_groups(
            agentId=agent_id,
            agentVersion='DRAFT'
        )
        
        # Find the duplicate action group to remove
        for ag in action_groups['actionGroupSummaries']:
            if ag['actionGroupName'] == 'product-analysis-functions':
                print(f"Disabling duplicate action group: {ag['actionGroupName']}")
                
                # Update to disable first
                bedrock.update_agent_action_group(
                    agentId=agent_id,
                    agentVersion='DRAFT',
                    actionGroupId=ag['actionGroupId'],
                    actionGroupName=ag['actionGroupName'],
                    actionGroupState='DISABLED'
                )
                
                print(f"Disabled: {ag['actionGroupName']}")
                
                # Now delete it
                bedrock.delete_agent_action_group(
                    agentId=agent_id,
                    agentVersion='DRAFT',
                    actionGroupId=ag['actionGroupId']
                )
                
                print(f"Deleted: {ag['actionGroupName']}")
        
        # Prepare agent
        bedrock.prepare_agent(agentId=agent_id)
        print("Agent prepared - duplicate removed")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_duplicate_actions()