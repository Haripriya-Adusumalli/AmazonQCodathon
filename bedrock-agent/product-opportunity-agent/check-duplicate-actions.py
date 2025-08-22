import boto3

def check_duplicate_actions():
    """Check for duplicate action groups calling same Lambda"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = 'DKPL7RP9OU'
    
    try:
        action_groups = bedrock.list_agent_action_groups(
            agentId=agent_id,
            agentVersion='DRAFT'
        )
        
        print("Current Action Groups:")
        lambda_functions = {}
        
        for ag in action_groups['actionGroupSummaries']:
            # Get action group details
            details = bedrock.get_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupId=ag['actionGroupId']
            )
            
            executor = details['agentActionGroup'].get('actionGroupExecutor', {})
            if 'lambda' in executor:
                lambda_arn = executor['lambda']
                func_name = lambda_arn.split(':')[-1]
                
                if func_name not in lambda_functions:
                    lambda_functions[func_name] = []
                lambda_functions[func_name].append(ag['actionGroupName'])
                
                print(f"  - {ag['actionGroupName']}: {func_name}")
        
        print("\nDuplicate Lambda calls:")
        for func, groups in lambda_functions.items():
            if len(groups) > 1:
                print(f"  {func} called by: {groups}")
                
                # Delete duplicate action groups (keep first one)
                for group_name in groups[1:]:
                    for ag in action_groups['actionGroupSummaries']:
                        if ag['actionGroupName'] == group_name:
                            bedrock.delete_agent_action_group(
                                agentId=agent_id,
                                agentVersion='DRAFT',
                                actionGroupId=ag['actionGroupId']
                            )
                            print(f"    Deleted duplicate: {group_name}")
        
        # Prepare agent after cleanup
        bedrock.prepare_agent(agentId=agent_id)
        print("Agent prepared after cleanup")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_duplicate_actions()