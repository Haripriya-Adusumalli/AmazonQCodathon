import boto3
import json
import time

def fix_and_prepare_agent():
    try:
        bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
        iam = boto3.client('iam')
        
        agent_id = 'E7QJOXGNCA'
        role_name = 'BedrockWeatherAgentRole'
        
        # Get role ARN
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
        print(f"Using role: {role_arn}")
        
        # Update agent with role
        print("Updating agent with role...")
        bedrock.update_agent(
            agentId=agent_id,
            agentName='weather-chat-agent',
            description='A helpful weather assistant that can chat about weather topics',
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
            instruction='You are a helpful weather assistant. You can discuss weather topics, provide general weather information, and help users understand weather patterns. Be friendly and informative.',
            agentResourceRoleArn=role_arn
        )
        
        print("Preparing agent...")
        bedrock.prepare_agent(agentId=agent_id)
        
        print("Waiting for preparation...")
        time.sleep(45)
        
        # Create alias
        try:
            alias_response = bedrock.create_agent_alias(
                agentId=agent_id,
                agentAliasName='live',
                description='Live version of the weather agent'
            )
            alias_id = alias_response['agentAlias']['agentAliasId']
            print(f"Created alias: {alias_id}")
        except Exception as e:
            print(f"Alias error: {e}")
            # Get existing aliases
            aliases = bedrock.list_agent_aliases(agentId=agent_id)
            if aliases['agentAliasSummaries']:
                alias_id = aliases['agentAliasSummaries'][0]['agentAliasId']
                print(f"Using existing alias: {alias_id}")
            else:
                alias_id = 'TSTALIASID'  # Default test alias
        
        # Save info
        agent_info = {
            'agentId': agent_id,
            'aliasId': alias_id,
            'region': 'us-east-1'
        }
        
        with open('agent-info.json', 'w') as f:
            json.dump(agent_info, f, indent=2)
        
        print(f"\\nAgent ready! ID: {agent_id}, Alias: {alias_id}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_and_prepare_agent()