import boto3
import json

def test_enhanced_agent():
    """Test the enhanced agent that React app uses"""
    
    bedrock = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    enhanced_agent_id = 'BKWEM7GZQX'  # From React config
    enhanced_alias_id = 'JPWRQS8CI3'  # From React config
    
    query = "Analyze smart water bottle opportunity"
    
    print(f"Testing enhanced agent: {enhanced_agent_id}")
    print(f"Query: {query}")
    
    try:
        response = bedrock.invoke_agent(
            agentId=enhanced_agent_id,
            agentAliasId=enhanced_alias_id,
            sessionId="test-session-enhanced",
            inputText=query
        )
        
        # Process response
        full_response = ""
        if response.get('completion'):
            for chunk in response['completion']:
                if chunk.get('chunk', {}).get('bytes'):
                    text = chunk['chunk']['bytes'].decode('utf-8')
                    full_response += text
                    print(text, end='', flush=True)
        
        print(f"\n\nResponse length: {len(full_response)} characters")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_enhanced_agent()