import boto3
import json
import time

def deploy_simple_product_agent():
    """Deploy a simplified product opportunity agent for demo"""
    
    print("🚀 Deploying Product Opportunity Agent...")
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    iam = boto3.client('iam')
    
    # Create IAM role
    role_name = 'ProductOpportunityAgentRole'
    
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
                "bedrock:InvokeModel"
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
        
        print("✅ Created IAM role")
        
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
        print("✅ Using existing IAM role")
    
    time.sleep(10)
    
    # Create agent with comprehensive instruction
    agent_instruction = """
    You are a Product Opportunity Orchestrator that identifies high-potential product opportunities using DCC analysis.
    
    When analyzing product opportunities, provide:
    
    1. DEMAND ANALYSIS (0-100 score):
    - Market interest and search trends
    - Consumer momentum and seasonality
    - Geographic demand patterns
    - Emerging market segments
    
    2. COMPETITION ANALYSIS (0-100 score, lower is better):
    - Market saturation level
    - Number of existing competitors
    - Average product ratings and reviews
    - Price competition intensity
    
    3. CAPABILITY ANALYSIS (0-100 score):
    - Required skills vs available expertise
    - Manufacturing/development readiness
    - Supply chain capabilities
    - Time to market estimation
    
    4. DCC SCORE CALCULATION:
    DCC = (Demand × 0.45) + ((100 - Competition) × 0.30) + (Capability × 0.25)
    
    5. RECOMMENDATIONS:
    - Specific differentiation strategies
    - Feature gaps to exploit
    - Market entry approach
    - Risk mitigation steps
    
    Always structure your response with clear sections and provide actionable insights.
    Include a JSON summary at the end with scores and key metrics.
    """
    
    try:
        agent_response = bedrock.create_agent(
            agentName='product-opportunity-analyzer',
            description='Analyzes product opportunities using DCC methodology',
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
            instruction=agent_instruction,
            agentResourceRoleArn=role_arn
        )
        
        agent_id = agent_response['agent']['agentId']
        print(f"✅ Created agent: {agent_id}")
        
        # Prepare agent
        print("⏳ Preparing agent...")
        bedrock.prepare_agent(agentId=agent_id)
        time.sleep(45)
        
        # Create alias
        try:
            alias_response = bedrock.create_agent_alias(
                agentId=agent_id,
                agentAliasName='live',
                description='Live product opportunity analyzer'
            )
            alias_id = alias_response['agentAlias']['agentAliasId']
            print(f"✅ Created alias: {alias_id}")
            
        except Exception as e:
            print(f"Alias creation failed: {e}")
            # Try to get existing alias
            try:
                aliases = bedrock.list_agent_aliases(agentId=agent_id)
                if aliases['agentAliasSummaries']:
                    alias_id = aliases['agentAliasSummaries'][0]['agentAliasId']
                    print(f"✅ Using existing alias: {alias_id}")
                else:
                    alias_id = 'TSTALIASID'
                    print("⚠️ Using test alias")
            except:
                alias_id = 'TSTALIASID'
                print("⚠️ Using test alias")
        
        # Save configuration
        config = {
            'agentId': agent_id,
            'aliasId': alias_id,
            'region': 'us-east-1',
            'roleArn': role_arn
        }
        
        with open('product-opportunity-config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\\n🎯 Product Opportunity Agent deployed successfully!")
        print(f"Agent ID: {agent_id}")
        print(f"Alias ID: {alias_id}")
        print("\\nUpdate your React app's aws-config.js with these values.")
        
        return config
        
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        return None

if __name__ == "__main__":
    deploy_simple_product_agent()