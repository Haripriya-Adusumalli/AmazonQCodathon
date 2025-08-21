import boto3
import json
import time

def create_orchestrator_agent():
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    iam = boto3.client('iam')
    
    role_name = 'ProductOpportunityOrchestratorRole'
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "bedrock.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    permissions_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeAgent",
                "dynamodb:*",
                "lambda:InvokeFunction"
            ],
            "Resource": "*"
        }]
    }
    
    try:
        role_response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        role_arn = role_response['Role']['Arn']
        
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName='ProductOpportunityPolicy',
            PolicyDocument=json.dumps(permissions_policy)
        )
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
    
    time.sleep(10)
    
    agent_instruction = """You are a Product Opportunity Orchestrator. Analyze product ideas and coordinate with domain agents to provide DCC scores (Demand + Competition + Capability). Break down requests and provide ranked recommendations."""
    
    try:
        agent_response = bedrock.create_agent(
            agentName='product-opportunity-orchestrator',
            description='Orchestrates product opportunity analysis',
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
            instruction=agent_instruction,
            agentResourceRoleArn=role_arn
        )
        
        agent_id = agent_response['agent']['agentId']
        bedrock.prepare_agent(agentId=agent_id)
        time.sleep(30)
        
        alias_response = bedrock.create_agent_alias(
            agentId=agent_id,
            agentAliasName='live'
        )
        
        alias_id = alias_response['agentAlias']['agentAliasId']
        
        config = {
            'orchestrator': {
                'agentId': agent_id,
                'aliasId': alias_id
            }
        }
        
        with open('product-agents-config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Orchestrator created: {agent_id}")
        return agent_id, alias_id
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    create_orchestrator_agent()