import boto3

def test_bedrock_agent():
    try:
        # Test with current AWS credentials
        client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
        
        print("Testing Bedrock agent access...")
        
        response = client.invoke_agent(
            agentId='E7QJOXGNCA',
            agentAliasId='JJYE1KNRVY',
            sessionId='test-session-123',
            inputText='Hello'
        )
        
        print("SUCCESS: Bedrock agent is accessible!")
        
        # Process response
        full_response = ""
        if 'completion' in response:
            for event in response['completion']:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        text = chunk['bytes'].decode('utf-8')
                        full_response += text
        
        print(f"Response: {full_response}")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_bedrock_agent()