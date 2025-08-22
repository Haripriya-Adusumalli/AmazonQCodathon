import boto3

def update_agent_instructions():
    """Update agent instructions to be more helpful"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    enhanced_agent_id = 'BKWEM7GZQX'  # Your enhanced agent
    
    new_instructions = """You are a Product Opportunity Analyzer that helps evaluate business opportunities using DCC (Demand + Competition + Capability) analysis.

Your role is to:
1. Analyze market demand for products using available market research tools
2. Evaluate competitive landscape and market saturation
3. Assess internal capabilities and readiness
4. Provide actionable recommendations with DCC scores

When users ask about product opportunities:
- Use your available analysis tools to gather data
- Calculate DCC scores based on the analysis
- Provide specific recommendations and next steps
- Be helpful and thorough in your analysis

You should actively use your analytical capabilities to provide valuable insights about product opportunities, market trends, and business recommendations."""

    try:
        bedrock.update_agent(
            agentId=enhanced_agent_id,
            agentName='Enhanced Product Opportunity Analyzer',
            description='AI agent that analyzes product opportunities using DCC methodology',
            instruction=new_instructions,
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0'
        )
        
        # Prepare agent
        bedrock.prepare_agent(agentId=enhanced_agent_id)
        
        print("Updated agent instructions to be more helpful")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_agent_instructions()