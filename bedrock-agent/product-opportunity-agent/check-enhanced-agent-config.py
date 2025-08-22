import boto3

def check_enhanced_agent_config():
    """Check enhanced agent configuration"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    enhanced_agent_id = 'BKWEM7GZQX'
    
    try:
        # Check agent details
        agent = bedrock.get_agent(agentId=enhanced_agent_id)
        print(f"Agent Name: {agent['agent']['agentName']}")
        print(f"Agent Status: {agent['agent']['agentStatus']}")
        
        # Check action groups
        action_groups = bedrock.list_agent_action_groups(
            agentId=enhanced_agent_id,
            agentVersion='DRAFT'
        )
        
        print(f"\nAction Groups: {len(action_groups['actionGroupSummaries'])}")
        for ag in action_groups['actionGroupSummaries']:
            print(f"  - {ag['actionGroupName']}: {ag['actionGroupState']}")
        
        if len(action_groups['actionGroupSummaries']) == 0:
            print("\n❌ No action groups found - agent won't use Lambda functions")
        else:
            print("\n✅ Action groups configured")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_enhanced_agent_config()