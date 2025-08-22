import boto3
import json

def test_agent_with_lambdas():
    """Test the Bedrock agent with Lambda function integration"""
    
    bedrock = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'
    alias_id = 'BIKYFE1L1K'
    
    test_queries = [
        "Analyze smart water bottle opportunity in India",
        "What's the potential for eco-friendly phone cases?",
        "Should we launch a fitness tracking app?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing: {query}")
        print('='*60)
        
        try:
            response = bedrock.invoke_agent(
                agentId=agent_id,
                agentAliasId=alias_id,
                sessionId=f"test-session-{hash(query)}",
                inputText=query
            )
            
            # Process response stream
            full_response = ""
            if response.get('completion'):
                for chunk in response['completion']:
                    if chunk.get('chunk', {}).get('bytes'):
                        text = chunk['chunk']['bytes'].decode('utf-8')
                        full_response += text
                        print(text, end='', flush=True)
            
            print(f"\n\nFull Response Length: {len(full_response)} characters")
            
        except Exception as e:
            print(f"Error testing query: {e}")
        
        print("\n" + "-"*60)

if __name__ == "__main__":
    test_agent_with_lambdas()