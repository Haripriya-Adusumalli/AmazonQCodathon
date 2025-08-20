import boto3
import json
import time

def create_bedrock_agent_with_role():
    try:
        # Initialize clients
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        account_id = identity['Account']
        print(f"Connected to AWS as: {identity['Arn']}")
        
        iam = boto3.client('iam')
        bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
        
        # Create IAM role for Bedrock agent
        role_name = 'BedrockWeatherAgentRole'
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "bedrock.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        try:
            role_response = iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description='Role for Bedrock Weather Agent'
            )
            role_arn = role_response['Role']['Arn']
            print(f"Created IAM role: {role_arn}")
        except iam.exceptions.EntityAlreadyExistsException:
            role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
            print(f"Using existing IAM role: {role_arn}")
        
        # Attach policy for Bedrock model invocation
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "bedrock:InvokeModel"
                    ],
                    "Resource": f"arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
                }
            ]
        }
        
        try:
            iam.put_role_policy(
                RoleName=role_name,
                PolicyName='BedrockModelInvokePolicy',
                PolicyDocument=json.dumps(policy_document)
            )
            print("Attached Bedrock model invoke policy")
        except Exception as e:
            print(f"Policy attachment (may already exist): {e}")
        
        # Wait for role to propagate
        print("Waiting for IAM role to propagate...")
        time.sleep(15)
        
        # Create Bedrock agent
        agent_response = bedrock.create_agent(
            agentName='weather-chat-agent',
            description='A helpful weather assistant that can chat about weather topics',
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
            instruction='You are a helpful weather assistant. You can discuss weather topics, provide general weather information, and help users understand weather patterns. Be friendly and informative.',
            agentResourceRoleArn=role_arn
        )
        
        agent_id = agent_response['agent']['agentId']
        print(f"Bedrock agent created with ID: {agent_id}")
        
        # Prepare the agent
        print("Preparing agent...")
        bedrock.prepare_agent(agentId=agent_id)
        
        # Wait for preparation
        print("Waiting for agent preparation...")
        time.sleep(30)
        
        # Create alias
        alias_response = bedrock.create_agent_alias(
            agentId=agent_id,
            agentAliasName='live',
            description='Live version of the weather agent'
        )
        
        alias_id = alias_response['agentAlias']['agentAliasId']
        print(f"Agent alias created with ID: {alias_id}")
        
        # Save agent info
        agent_info = {
            'agentId': agent_id,
            'aliasId': alias_id,
            'region': 'us-east-1'
        }
        
        with open('agent-info.json', 'w') as f:
            json.dump(agent_info, f, indent=2)
        
        print("\\nAgent deployment complete!")
        print(f"Agent ID: {agent_id}")
        print(f"Alias ID: {alias_id}")
        
        return agent_id, alias_id
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    create_bedrock_agent_with_role()