import json
import boto3

def lambda_handler(event, context):
    """Capability Match Agent - analyzes internal readiness using Q Business"""
    
    try:
        query = event.get('query', '')
        required_skills = event.get('required_skills', [])
        
        # Mock Q Business integration (replace with actual Q Business API)
        capability_analysis = analyze_mock_capabilities(query, required_skills)
        
        # Calculate capability score
        capability_score = calculate_capability_score(capability_analysis)
        
        result = {
            'capability_score': round(capability_score, 2),
            'skill_matches': capability_analysis['skill_matches'],
            'skill_gaps': capability_analysis['skill_gaps'],
            'supplier_readiness': capability_analysis['supplier_readiness'],
            'time_to_market': capability_analysis['time_to_market'],
            'compliance_status': capability_analysis['compliance_status'],
            'recommended_actions': capability_analysis['recommended_actions']
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def analyze_mock_capabilities(query, required_skills):
    """Mock capability analysis using simulated internal knowledge base"""
    
    # Simulate internal capabilities based on query type
    query_lower = query.lower()
    
    # Mock skill database
    available_skills = [
        "product design", "manufacturing", "supply chain", "marketing", 
        "software development", "hardware engineering", "quality assurance",
        "regulatory compliance", "customer support", "data analytics"
    ]
    
    # Determine skill matches based on query
    if "software" in query_lower or "app" in query_lower:
        skill_matches = ["software development", "data analytics", "customer support"]
        skill_gaps = ["hardware engineering", "manufacturing"]
        supplier_readiness = "High"
        time_to_market = "3-6 months"
    elif "hardware" in query_lower or "device" in query_lower:
        skill_matches = ["hardware engineering", "manufacturing", "quality assurance"]
        skill_gaps = ["software development", "regulatory compliance"]
        supplier_readiness = "Medium"
        time_to_market = "6-12 months"
    else:
        skill_matches = ["product design", "marketing", "supply chain"]
        skill_gaps = ["specialized expertise"]
        supplier_readiness = "Medium"
        time_to_market = "4-8 months"
    
    # Mock compliance status
    compliance_status = {
        "regulatory": "Needs Review",
        "safety": "Compliant",
        "environmental": "Compliant"
    }
    
    # Generate recommendations
    recommended_actions = []
    if skill_gaps:
        recommended_actions.append(f"Hire expertise in: {', '.join(skill_gaps[:2])}")
    if supplier_readiness != "High":
        recommended_actions.append("Evaluate supplier partnerships")
    recommended_actions.append("Conduct market validation study")
    
    return {
        'skill_matches': skill_matches,
        'skill_gaps': skill_gaps,
        'supplier_readiness': supplier_readiness,
        'time_to_market': time_to_market,
        'compliance_status': compliance_status,
        'recommended_actions': recommended_actions
    }

def calculate_capability_score(analysis):
    """Calculate capability score (0-100)"""
    
    # Score based on skill matches vs gaps
    skill_ratio = len(analysis['skill_matches']) / max(1, len(analysis['skill_matches']) + len(analysis['skill_gaps']))
    
    # Supplier readiness factor
    supplier_map = {'High': 1.0, 'Medium': 0.7, 'Low': 0.4}
    supplier_factor = supplier_map.get(analysis['supplier_readiness'], 0.5)
    
    # Time to market factor (shorter is better)
    time_factor = 0.9 if "3-6" in analysis['time_to_market'] else 0.7
    
    capability_score = (skill_ratio * 50) + (supplier_factor * 30) + (time_factor * 20)
    
    return max(0, min(100, capability_score))