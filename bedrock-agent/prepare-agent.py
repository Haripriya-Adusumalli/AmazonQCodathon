import boto3
import json
import time

def prepare_and_setup_agent():
    try:
        bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
        agent_id = 'E7QJOXGNCA'  # The existing agent ID
        
        print(f"Preparing agent {agent_id}...")
        bedrock.prepare_agent(agentId=agent_id)
        
        # Wait for preparation
        print("Waiting for agent preparation (this may take a minute)...")
        time.sleep(60)
        
        # Check agent status
        agent_details = bedrock.get_agent(agentId=agent_id)
        print(f"Agent status: {agent_details['agent']['agentStatus']}")
        
        # Create alias
        try:
            alias_response = bedrock.create_agent_alias(
                agentId=agent_id,
                agentAliasName='live',
                description='Live version of the weather agent'
            )
            alias_id = alias_response['agentAlias']['agentAliasId']
            print(f"Created alias with ID: {alias_id}")
        except Exception as e:
            print(f"Alias creation error (may already exist): {e}")
            # Try to get existing alias
            aliases = bedrock.list_agent_aliases(agentId=agent_id)
            alias_id = None
            for alias in aliases['agentAliasSummaries']:
                if alias['agentAliasName'] == 'live':
                    alias_id = alias['agentAliasId']
                    break
            if not alias_id and aliases['agentAliasSummaries']:
                alias_id = aliases['agentAliasSummaries'][0]['agentAliasId']
        
        # Save agent info
        agent_info = {
            'agentId': agent_id,
            'aliasId': alias_id,
            'region': 'us-east-1'
        }
        
        with open('agent-info.json', 'w') as f:
            json.dump(agent_info, f, indent=2)
        
        print("\\nAgent setup complete!")
        print(f"Agent ID: {agent_id}")
        print(f"Alias ID: {alias_id}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    prepare_and_setup_agent()