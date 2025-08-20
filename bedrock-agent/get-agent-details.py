import boto3
import json

def get_agent_details():
    try:
        bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
        
        # Get agent details
        agent_id = 'E7QJOXGNCA'
        agent_details = bedrock.get_agent(agentId=agent_id)
        
        print("Agent Details:")
        print(f"  Name: {agent_details['agent']['agentName']}")
        print(f"  ID: {agent_details['agent']['agentId']}")
        print(f"  Status: {agent_details['agent']['agentStatus']}")
        print(f"  Description: {agent_details['agent'].get('description', 'N/A')}")
        print(f"  Foundation Model: {agent_details['agent'].get('foundationModel', 'N/A')}")
        
        # Get aliases
        print("\nAgent Aliases:")
        aliases = bedrock.list_agent_aliases(agentId=agent_id)
        
        if aliases['agentAliasSummaries']:
            for alias in aliases['agentAliasSummaries']:
                print(f"  - Name: {alias['agentAliasName']}")
                print(f"    ID: {alias['agentAliasId']}")
                print(f"    Status: {alias['agentAliasStatus']}")
        else:
            print("  No aliases found")
            
        # Save current agent info
        if aliases['agentAliasSummaries']:
            alias_id = aliases['agentAliasSummaries'][0]['agentAliasId']
            agent_info = {
                'agentId': agent_id,
                'aliasId': alias_id,
                'region': 'us-east-1',
                'status': agent_details['agent']['agentStatus']
            }
            
            with open('agent-info.json', 'w') as f:
                json.dump(agent_info, f, indent=2)
            
            print(f"\nAgent is ready to use!")
            print(f"Agent ID: {agent_id}")
            print(f"Alias ID: {alias_id}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_agent_details()