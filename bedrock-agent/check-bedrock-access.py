import boto3
import json

def check_bedrock_access():
    try:
        # Check if we can access Bedrock service
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        
        print("Checking Bedrock access...")
        
        # Try to list foundation models
        try:
            models = bedrock.list_foundation_models()
            print(f"✓ Can access Bedrock service")
            print(f"✓ Found {len(models['modelSummaries'])} foundation models")
            
            # Check for Claude models
            claude_models = [m for m in models['modelSummaries'] if 'claude' in m['modelId'].lower()]
            if claude_models:
                print(f"✓ Found {len(claude_models)} Claude models")
                for model in claude_models[:3]:
                    print(f"  - {model['modelId']}")
            else:
                print("✗ No Claude models found")
                
        except Exception as e:
            print(f"✗ Cannot access Bedrock models: {e}")
            print("\nYou may need to:")
            print("1. Enable model access in Bedrock console")
            print("2. Go to AWS Console > Bedrock > Model access")
            print("3. Request access to Claude models")
            return False
        
        # Test direct model invocation
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        try:
            test_payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 100,
                "messages": [
                    {"role": "user", "content": "Hello, say hi back"}
                ]
            }
            
            response = bedrock_runtime.invoke_model(
                modelId='anthropic.claude-3-haiku-20240307-v1:0',
                body=json.dumps(test_payload),
                contentType='application/json'
            )
            
            print("✓ Can invoke Claude model directly")
            return True
            
        except Exception as e:
            print(f"✗ Cannot invoke Claude model: {e}")
            if "access" in str(e).lower():
                print("\nYou need to request model access:")
                print("1. Go to AWS Console > Amazon Bedrock")
                print("2. Click 'Model access' in the left sidebar")
                print("3. Click 'Request model access'")
                print("4. Select 'Anthropic Claude 3 Haiku' and submit request")
            return False
            
    except Exception as e:
        print(f"Error checking Bedrock access: {e}")
        return False

if __name__ == "__main__":
    check_bedrock_access()