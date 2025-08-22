import boto3

def fix_agent_instructions():
    """Fix agent instructions with proper parameters"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    enhanced_agent_id = 'BKWEM7GZQX'
    
    # Get current agent details
    agent = bedrock.get_agent(agentId=enhanced_agent_id)
    current_agent = agent['agent']
    
    new_instructions = """You are a Product Opportunity Analyzer that helps evaluate business opportunities using DCC (Demand + Competition + Capability) analysis.

Your role is to:
1. Analyze market demand for products using your market analysis capabilities
2. Evaluate competitive landscape and market saturation  
3. Assess internal capabilities and readiness
4. Provide actionable recommendations with DCC scores

When users ask about product opportunities, you should:
- Use your analytical tools to gather market data
- Calculate DCC scores based on demand, competition, and capability analysis
- Provide specific recommendations and next steps
- Be helpful and thorough in your analysis

Always use your available tools to provide valuable insights about product opportunities, market trends, and business recommendations."""

    try:
        bedrock.update_agent(
            agentId=enhanced_agent_id,
            agentName=current_agent['agentName'],
            description=current_agent.get('description', 'Product Opportunity Analyzer'),
            instruction=new_instructions,
            foundationModel=current_agent['foundationModel'],
            agentResourceRoleArn=current_agent['agentResourceRoleArn']
        )
        
        # Prepare agent
        bedrock.prepare_agent(agentId=enhanced_agent_id)
        
        print("Updated agent instructions successfully")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_agent_instructions()