import boto3
import json

def test_agent_no_approval():
    """Test if agent works without approval prompts"""
    
    bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'
    alias_id = 'BIKYFE1L1K'
    
    # Test query
    query = "Analyze the opportunity for smart water bottles in the US market"
    
    print(f"Testing agent with query: {query}")
    print("Checking if approval prompts appear...")
    
    try:
        response = bedrock_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=alias_id,
            sessionId='test-session-no-approval',
            inputText=query
        )
        
        # Process response
        response_text = ""
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    response_text += chunk['bytes'].decode('utf-8')
        
        print("\\n=== AGENT RESPONSE ===")
        print(response_text)
        
        # Check for approval-related keywords
        approval_keywords = ['approve', 'confirm', 'permission', 'authorize', 'allow me to']
        found_approval = any(keyword.lower() in response_text.lower() for keyword in approval_keywords)
        
        if found_approval:
            print("\\n❌ APPROVAL PROMPTS STILL PRESENT")
            print("The agent is still asking for approval.")
        else:
            print("\\n✅ NO APPROVAL PROMPTS DETECTED")
            print("The agent executed without asking for approval!")
            
    except Exception as e:
        print(f"Error testing agent: {e}")

if __name__ == "__main__":
    test_agent_no_approval()