import boto3

def test_original_agent():
    """Test the original agent to ensure it's working"""
    
    bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'
    alias_id = 'NTC6Q4Y2BZ'
    
    query = "Analyze smart water bottle opportunity in India"
    
    print(f"Testing original agent: {agent_id}")
    print(f"Query: {query}")
    
    try:
        response = bedrock_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=alias_id,
            sessionId='test-original-fixed',
            inputText=query
        )
        
        response_text = ""
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    response_text += chunk['bytes'].decode('utf-8')
        
        print("\\n=== ORIGINAL AGENT RESPONSE ===")
        print(response_text)
        print("\\nOriginal agent is working!")
        
    except Exception as e:
        print(f"Original agent still failing: {e}")

if __name__ == "__main__":
    test_original_agent()