import boto3
import json

def fix_bedrock_permissions():
    try:
        iam = boto3.client('iam')
        bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
        
        role_name = 'BedrockWeatherAgentRole'
        
        # Update the policy to include proper Bedrock permissions
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "bedrock:InvokeModel",
                        "bedrock:InvokeModelWithResponseStream"
                    ],
                    "Resource": [
                        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
                        "arn:aws:bedrock:*::foundation-model/*"
                    ]
                }
            ]
        }
        
        # Update the role policy
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName='BedrockModelInvokePolicy',
            PolicyDocument=json.dumps(policy_document)
        )
        
        print("Updated IAM role permissions for Bedrock model invocation")
        
        # Get the role ARN
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
        
        # Update the agent to ensure it has the correct role
        agent_id = 'E7QJOXGNCA'
        bedrock.update_agent(
            agentId=agent_id,
            agentName='weather-chat-agent',
            description='A helpful weather assistant that can chat about weather topics',
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
            instruction='You are a helpful weather assistant. You can discuss weather topics, provide general weather information, and help users understand weather patterns. Be friendly and informative.',
            agentResourceRoleArn=role_arn
        )
        
        print("Updated agent with correct role")
        
        # Prepare the agent again
        print("Preparing agent...")
        bedrock.prepare_agent(agentId=agent_id)
        
        print("Agent permissions fixed! Wait 30 seconds before testing.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_bedrock_permissions()