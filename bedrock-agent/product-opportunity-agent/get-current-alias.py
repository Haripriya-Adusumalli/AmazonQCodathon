import boto3
import json

def get_current_alias():
    """Get the current agent alias ID"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = 'DKPL7RP9OU'
    
    try:
        # List agent aliases
        response = bedrock.list_agent_aliases(agentId=agent_id)
        
        print("Current agent aliases:")
        for alias in response['agentAliasSummaries']:
            print(f"Alias ID: {alias['agentAliasId']}")
            print(f"Alias Name: {alias['agentAliasName']}")
            print(f"Status: {alias.get('agentAliasStatus', 'Unknown')}")
            print(f"Created: {alias.get('createdAt', 'Unknown')}")
            print("---")
        
        # Get the most recent alias
        if response['agentAliasSummaries']:
            latest_alias = response['agentAliasSummaries'][0]
            alias_id = latest_alias['agentAliasId']
            
            print(f"\\nLatest alias ID to use: {alias_id}")
            
            # Update the config file
            config = {
                'agentId': agent_id,
                'aliasId': alias_id,
                'region': 'us-east-1'
            }
            
            with open('product-opportunity-config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            print("Updated product-opportunity-config.json")
            return alias_id
        else:
            print("No aliases found!")
            return None
            
    except Exception as e:
        print(f"Error getting aliases: {e}")
        return None

if __name__ == "__main__":
    get_current_alias()