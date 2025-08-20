import boto3
import json

def simple_bedrock_check():
    try:
        print("Checking Bedrock access...")
        
        # Check Bedrock service
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        models = bedrock.list_foundation_models()
        print(f"SUCCESS: Can access Bedrock service")
        print(f"Found {len(models['modelSummaries'])} foundation models")
        
        # Check for Claude models
        claude_models = [m for m in models['modelSummaries'] if 'claude' in m['modelId'].lower()]
        print(f"Found {len(claude_models)} Claude models")
        
        if not claude_models:
            print("ERROR: No Claude models available")
            print("You need to request model access in AWS Console")
            return False
        
        # Test model invocation
        print("Testing Claude model invocation...")
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        test_payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 50,
            "messages": [{"role": "user", "content": "Say hello"}]
        }
        
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps(test_payload),
            contentType='application/json'
        )
        
        print("SUCCESS: Can invoke Claude model")
        
        # Parse response
        response_body = json.loads(response['body'].read())
        print(f"Model response: {response_body['content'][0]['text']}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        if "access" in str(e).lower() or "denied" in str(e).lower():
            print("\nYou need to enable model access:")
            print("1. Go to AWS Console > Amazon Bedrock")
            print("2. Click 'Model access' in left sidebar")
            print("3. Click 'Request model access'")
            print("4. Select Claude models and submit request")
        return False

if __name__ == "__main__":
    simple_bedrock_check()