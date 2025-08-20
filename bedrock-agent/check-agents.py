import boto3
import json

def check_bedrock_agents():
    try:
        # Verify AWS credentials
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"Connected to AWS as: {identity['Arn']}")
        print(f"Account ID: {identity['Account']}")
        
        # Check Bedrock agent service
        bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
        
        print("\nListing existing agents...")
        agents = bedrock.list_agents()
        
        if agents['agentSummaries']:
            print(f"Found {len(agents['agentSummaries'])} agents:")
            for agent in agents['agentSummaries']:
                print(f"  - Name: {agent['agentName']}")
                print(f"    ID: {agent['agentId']}")
                print(f"    Status: {agent['agentStatus']}")
                print(f"    Created: {agent['createdAt']}")
                print()
        else:
            print("No agents found in your account.")
            
        # Check available foundation models
        print("Checking available foundation models...")
        bedrock_models = boto3.client('bedrock', region_name='us-east-1')
        models = bedrock_models.list_foundation_models()
        
        claude_models = [m for m in models['modelSummaries'] if 'claude' in m['modelId'].lower()]
        print(f"Found {len(claude_models)} Claude models available:")
        for model in claude_models[:3]:  # Show first 3
            print(f"  - {model['modelId']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_bedrock_agents()