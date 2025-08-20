import boto3
import json

def get_existing_agent():
    try:
        bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
        
        # List agents
        agents = bedrock.list_agents()
        
        for agent in agents['agentSummaries']:
            if agent['agentName'] == 'weather-chat-agent':
                agent_id = agent['agentId']
                print(f"Found agent: {agent['agentName']} with ID: {agent_id}")
                
                # List aliases
                aliases = bedrock.list_agent_aliases(agentId=agent_id)
                
                alias_id = None
                for alias in aliases['agentAliasSummaries']:
                    if alias['agentAliasName'] == 'live':
                        alias_id = alias['agentAliasId']
                        break
                
                if not alias_id:
                    # Create alias if it doesn't exist
                    alias_response = bedrock.create_agent_alias(
                        agentId=agent_id,
                        agentAliasName='live',
                        description='Live version of the weather agent'
                    )
                    alias_id = alias_response['agentAlias']['agentAliasId']
                    print(f"Created alias with ID: {alias_id}")
                else:
                    print(f"Found alias with ID: {alias_id}")
                
                # Save agent info
                agent_info = {
                    'agentId': agent_id,
                    'aliasId': alias_id,
                    'region': 'us-east-1'
                }
                
                with open('agent-info.json', 'w') as f:
                    json.dump(agent_info, f, indent=2)
                
                print("Agent info saved to agent-info.json")
                return agent_id, alias_id
        
        print("Agent not found")
        return None, None
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    get_existing_agent()