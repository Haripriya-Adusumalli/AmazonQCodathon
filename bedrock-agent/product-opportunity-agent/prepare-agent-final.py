import boto3
import time

def prepare_agent_final():
    """Final agent preparation to ensure action groups work"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = 'DKPL7RP9OU'
    
    # Check current agent status
    agent = bedrock.get_agent(agentId=agent_id)
    print(f"Agent status: {agent['agent']['agentStatus']}")
    
    # Prepare agent
    print("Preparing agent...")
    bedrock.prepare_agent(agentId=agent_id)
    
    # Wait for preparation
    print("Waiting for preparation...")
    time.sleep(60)
    
    # Check status again
    agent = bedrock.get_agent(agentId=agent_id)
    print(f"Agent status after preparation: {agent['agent']['agentStatus']}")
    
    # Update alias to point to latest version
    try:
        aliases = bedrock.list_agent_aliases(agentId=agent_id)
        if aliases['agentAliasSummaries']:
            alias_id = aliases['agentAliasSummaries'][0]['agentAliasId']
            
            bedrock.update_agent_alias(
                agentId=agent_id,
                agentAliasId=alias_id,
                agentAliasName='live',
                description='Live agent with Lambda functions'
            )
            print(f"Updated alias: {alias_id}")
    
    except Exception as e:
        print(f"Error updating alias: {e}")

if __name__ == "__main__":
    prepare_agent_final()