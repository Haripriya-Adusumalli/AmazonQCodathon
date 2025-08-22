import boto3
import json

def check_agent_configuration():
    """Check the agent's action groups and permissions"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'
    
    # Check agent action groups
    try:
        action_groups = bedrock.list_agent_action_groups(
            agentId=agent_id,
            agentVersion='DRAFT'
        )
        
        print("Agent Action Groups:")
        for ag in action_groups['actionGroupSummaries']:
            print(f"  - {ag['actionGroupName']}: {ag['actionGroupState']}")
            
    except Exception as e:
        print(f"Error checking action groups: {e}")
    
    # Check Lambda permissions for Bedrock
    lambda_functions = ['market-demand-agent', 'competitor-scan-agent', 'capability-match-agent']
    
    for func_name in lambda_functions:
        try:
            policy = lambda_client.get_policy(FunctionName=func_name)
            print(f"\n{func_name} has resource policy")
        except lambda_client.exceptions.ResourceNotFoundException:
            print(f"\n{func_name} has NO resource policy - needs Bedrock permission")
            
            # Add permission for Bedrock to invoke Lambda
            try:
                lambda_client.add_permission(
                    FunctionName=func_name,
                    StatementId='bedrock-invoke',
                    Action='lambda:InvokeFunction',
                    Principal='bedrock.amazonaws.com',
                    SourceArn=f'arn:aws:bedrock:us-east-1:*:agent/{agent_id}'
                )
                print(f"  Added Bedrock permission to {func_name}")
            except Exception as e:
                print(f"  Error adding permission: {e}")

if __name__ == "__main__":
    check_agent_configuration()