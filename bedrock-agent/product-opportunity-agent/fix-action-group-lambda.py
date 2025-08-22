import boto3

def fix_action_group_lambda():
    """Fix action group to point to correct Lambda function"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'
    
    # Get correct Lambda ARN
    correct_lambda_arn = lambda_client.get_function(FunctionName='market-demand-agent')['Configuration']['FunctionArn']
    
    try:
        # List current action groups
        action_groups = bedrock.list_agent_action_groups(
            agentId=agent_id,
            agentVersion='DRAFT'
        )
        
        for ag in action_groups['actionGroupSummaries']:
            # Get action group details
            details = bedrock.get_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupId=ag['actionGroupId']
            )
            
            current_lambda = details['agentActionGroup'].get('actionGroupExecutor', {}).get('lambda', '')
            print(f"Action group '{ag['actionGroupName']}' currently points to: {current_lambda}")
            
            if 'enhanced-market-demand-copy' in current_lambda:
                print(f"Updating {ag['actionGroupName']} to point to correct Lambda")
                
                # Update action group to point to correct Lambda
                bedrock.update_agent_action_group(
                    agentId=agent_id,
                    agentVersion='DRAFT',
                    actionGroupId=ag['actionGroupId'],
                    actionGroupName=ag['actionGroupName'],
                    actionGroupExecutor={
                        'lambda': correct_lambda_arn
                    },
                    apiSchema=details['agentActionGroup']['apiSchema']
                )
                
                print(f"Updated {ag['actionGroupName']} to use: {correct_lambda_arn}")
        
        # Prepare agent
        bedrock.prepare_agent(agentId=agent_id)
        print("Agent prepared with correct Lambda reference")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_action_group_lambda()