import boto3
import json
import time

def create_simple_bedrock_agent():
    try:
        # Verify AWS credentials
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"Connected to AWS as: {identity['Arn']}")
        
        bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
        
        # Create a simple agent without Lambda for now
        agent_response = bedrock.create_agent(
            agentName='weather-chat-agent',
            description='A helpful weather assistant that can chat about weather topics',
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
            instruction='You are a helpful weather assistant. You can discuss weather topics, provide general weather information, and help users understand weather patterns. Be friendly and informative.'
        )
        
        agent_id = agent_response['agent']['agentId']
        print(f"Bedrock agent created with ID: {agent_id}")
        
        # Prepare the agent
        print("Preparing agent...")
        bedrock.prepare_agent(agentId=agent_id)
        
        # Wait for preparation to complete
        time.sleep(30)
        
        # Create alias
        alias_response = bedrock.create_agent_alias(
            agentId=agent_id,
            agentAliasName='live',
            description='Live version of the weather agent'
        )
        
        alias_id = alias_response['agentAlias']['agentAliasId']
        print(f"Agent alias created with ID: {alias_id}")
        
        # Save agent info to file
        agent_info = {
            'agentId': agent_id,
            'aliasId': alias_id,
            'region': 'us-east-1'
        }
        
        with open('agent-info.json', 'w') as f:
            json.dump(agent_info, f, indent=2)
        
        print("Agent deployment complete!")
        print(f"Agent ID: {agent_id}")
        print(f"Alias ID: {alias_id}")
        
        return agent_id, alias_id
        
    except Exception as e:
        print(f"Error creating agent: {e}")
        return None, None

if __name__ == "__main__":
    create_simple_bedrock_agent()