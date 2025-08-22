import boto3

def test_new_alias():
    """Test the new opportunityagent alias"""
    
    bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'
    alias_id = 'NTC6Q4Y2BZ'
    
    query = "Analyze smart water bottle opportunity in India"
    
    print(f"Testing agent with new alias: {alias_id}")
    print(f"Query: {query}")
    
    try:
        response = bedrock_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=alias_id,
            sessionId='test-new-alias',
            inputText=query
        )
        
        response_text = ""
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    response_text += chunk['bytes'].decode('utf-8')
        
        print("\\n=== RESPONSE ===")
        print(response_text)
        print("\\n✅ Test successful!")
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_new_alias()