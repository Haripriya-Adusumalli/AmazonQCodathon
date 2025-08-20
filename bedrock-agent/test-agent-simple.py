import boto3
import time

def test_agent():
    try:
        client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
        
        print("Testing Bedrock agent...")
        
        response = client.invoke_agent(
            agentId='E7QJOXGNCA',
            agentAliasId='JJYE1KNRVY',
            sessionId=f'test-session-{int(time.time())}',
            inputText='Hello! Tell me about sunny weather.'
        )
        
        # Process the response stream
        full_response = ""
        if 'completion' in response:
            for event in response['completion']:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        text = chunk['bytes'].decode('utf-8')
                        full_response += text
                        print(text, end='', flush=True)
        
        print(f"\n\nFull response: {full_response}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Wait a bit for the agent to be ready
    print("Waiting 30 seconds for agent to be ready...")
    time.sleep(30)
    test_agent()