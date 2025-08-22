import boto3

def test_enhanced_agent_final():
    """Test the enhanced agent with all three Lambda functions"""
    
    bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    agent_id = 'BKWEM7GZQX'
    alias_id = 'JPWRQS8CI3'
    
    query = "Analyze smart fitness tracker opportunity in US market"
    
    print(f"Testing enhanced agent: {agent_id}")
    print(f"Query: {query}")
    print("This should call all three enhanced Lambda functions...")
    
    try:
        response = bedrock_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=alias_id,
            sessionId='test-enhanced-final',
            inputText=query
        )
        
        response_text = ""
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    response_text += chunk['bytes'].decode('utf-8')
        
        print("\\n=== ENHANCED AGENT RESPONSE ===")
        print(response_text)
        
        # Check if it mentions all three analyses
        has_demand = any(word in response_text.lower() for word in ['demand', 'interest', 'trends'])
        has_competition = any(word in response_text.lower() for word in ['competition', 'competitors', 'market saturation'])
        has_capability = any(word in response_text.lower() for word in ['capability', 'skills', 'readiness'])
        
        print(f"\\n=== ANALYSIS CHECK ===")
        print(f"Demand analysis detected: {has_demand}")
        print(f"Competition analysis detected: {has_competition}")
        print(f"Capability analysis detected: {has_capability}")
        
        if has_demand and has_competition and has_capability:
            print("\\n✅ SUCCESS: All three analyses appear to be working!")
        else:
            print("\\n⚠️ PARTIAL: Some analyses may not be working properly")
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_enhanced_agent_final()