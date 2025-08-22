import boto3

def get_alias_id():
    """Get the correct alias ID"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = 'DKPL7RP9OU'
    
    try:
        response = bedrock.list_agent_aliases(agentId=agent_id)
        
        print("Available aliases:")
        for alias in response['agentAliasSummaries']:
            print(f"Name: {alias['agentAliasName']}")
            print(f"ID: {alias['agentAliasId']}")
            print(f"Status: {alias.get('agentAliasStatus', 'Unknown')}")
            print("---")
        
        # Find the opportunityagent alias
        for alias in response['agentAliasSummaries']:
            if alias['agentAliasName'] == 'opportunityagent':
                print(f"\\nCorrect alias ID for 'opportunityagent': {alias['agentAliasId']}")
                return alias['agentAliasId']
        
        print("\\nAlias 'opportunityagent' not found!")
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    get_alias_id()