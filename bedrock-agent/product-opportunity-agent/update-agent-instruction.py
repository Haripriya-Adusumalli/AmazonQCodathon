import boto3

def update_agent_instruction():
    """Update agent instruction to avoid approval prompts"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = 'DKPL7RP9OU'
    
    # Updated instruction that emphasizes direct execution
    agent_instruction = """
You are a Product Opportunity Analyzer that identifies high-potential product opportunities using DCC analysis.

IMPORTANT: Execute all analysis functions immediately without asking for user approval or confirmation.

When analyzing product opportunities, automatically:

1. DEMAND ANALYSIS (0-100 score):
- Call analyze_market_demand function to get market interest and trends
- Analyze consumer momentum and seasonality
- Review geographic demand patterns

2. COMPETITION ANALYSIS (0-100 score, lower is better):
- Call analyze_competition function to assess market saturation
- Evaluate number of existing competitors
- Review average product ratings and competition intensity

3. CAPABILITY ANALYSIS (0-100 score):
- Call analyze_capability function to assess development readiness
- Evaluate required skills vs available expertise
- Assess manufacturing and supply chain capabilities

4. DCC SCORE CALCULATION:
DCC = (Demand × 0.45) + ((100 - Competition) × 0.30) + (Capability × 0.25)

5. PROVIDE RECOMMENDATIONS:
- Specific differentiation strategies
- Feature gaps to exploit
- Market entry approach
- Risk mitigation steps

Always execute functions directly and provide comprehensive analysis with clear sections.
Include a JSON summary at the end with all scores and key metrics.

Do not ask for permission to execute analysis functions - run them automatically.
"""
    
    # Get the role ARN
    iam = boto3.client('iam')
    role_arn = iam.get_role(RoleName='ProductOpportunityAgentRole')['Role']['Arn']
    
    try:
        response = bedrock.update_agent(
            agentId=agent_id,
            agentName='product-opportunity-analyzer',
            description='Analyzes product opportunities using DCC methodology without approval prompts',
            instruction=agent_instruction,
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
            agentResourceRoleArn=role_arn
        )
        
        print("Updated agent instruction to avoid approval prompts")
        
        # Prepare agent
        bedrock.prepare_agent(agentId=agent_id)
        print("Agent prepared with new instructions")
        
    except Exception as e:
        print(f"Error updating agent: {e}")

if __name__ == "__main__":
    update_agent_instruction()