import boto3
import time

def force_delete_duplicate():
    """Force delete duplicate action group"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = 'DKPL7RP9OU'
    
    try:
        action_groups = bedrock.list_agent_action_groups(
            agentId=agent_id,
            agentVersion='DRAFT'
        )
        
        for ag in action_groups['actionGroupSummaries']:
            if ag['actionGroupName'] == 'product-analysis-functions':
                print(f"Force deleting: {ag['actionGroupName']}")
                
                try:
                    bedrock.delete_agent_action_group(
                        agentId=agent_id,
                        agentVersion='DRAFT',
                        actionGroupId=ag['actionGroupId'],
                        skipResourceInUseCheck=True
                    )
                    print(f"Deleted: {ag['actionGroupName']}")
                except Exception as e:
                    print(f"Delete failed: {e}")
        
        time.sleep(5)
        
        # Prepare agent
        bedrock.prepare_agent(agentId=agent_id)
        print("Agent prepared")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    force_delete_duplicate()