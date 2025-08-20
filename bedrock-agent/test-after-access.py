import boto3
import json
import time

def test_after_model_access():
    try:
        print("Testing Bedrock after model access...")
        
        # Test direct model invocation first
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        test_payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [{"role": "user", "content": "Hello! Tell me about weather in one sentence."}]
        }
        
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps(test_payload),
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        print(f"Direct model test SUCCESS: {response_body['content'][0]['text']}")
        
        # Now test the agent
        print("\nTesting Bedrock agent...")
        client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
        
        response = client.invoke_agent(
            agentId='E7QJOXGNCA',
            agentAliasId='JJYE1KNRVY',
            sessionId=f'test-session-{int(time.time())}',
            inputText='Hello! Tell me about sunny weather.'
        )
        
        # Process response
        full_response = ""
        if 'completion' in response:
            for event in response['completion']:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        text = chunk['bytes'].decode('utf-8')
                        full_response += text
        
        print(f"Agent test SUCCESS: {full_response}")
        print("\nYour Bedrock agent is now working!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        if "access" in str(e).lower():
            print("Still need to enable model access in AWS Console")

if __name__ == "__main__":
    test_after_model_access()