import json

def lambda_handler(event, context):
    """Enhanced Capability Match Agent with correct Bedrock response format"""
    
    try:
        # Handle Bedrock agent input format
        if 'inputText' in event:
            query = event['inputText']
            required_skills = []
        elif 'parameters' in event:
            params = event['parameters']
            query = params.get('query', '')
            required_skills = params.get('required_skills', [])
        else:
            query = event.get('query', '')
            required_skills = event.get('required_skills', [])
        
        # Enhanced capability analysis
        capability_data = get_internal_capabilities(query)
        supplier_data = get_supplier_capabilities(query)
        capability_analysis = analyze_capabilities(query, capability_data, supplier_data, required_skills)
        
        result = {
            'capability_score': capability_analysis['score'],
            'skill_matches': capability_analysis['skill_matches'],
            'skill_gaps': capability_analysis['skill_gaps'],
            'internal_readiness': capability_analysis['internal_readiness'],
            'supplier_readiness': capability_analysis['supplier_readiness'],
            'time_to_market': capability_analysis['time_to_market'],
            'compliance_status': capability_analysis['compliance_status'],
            'recommended_actions': capability_analysis['recommended_actions'],
            'risk_factors': capability_analysis['risk_factors'],
            'data_source': 'enhanced_analysis'
        }
        
        # Return in Bedrock action group format
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup', 'enhanced-capability-analysis'),
                "function": event.get('function'),
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps(result)
                        }
                    }
                }
            },
            "sessionAttributes": {},
            "promptSessionAttributes": {}
        }
        
    except Exception as e:
        error_result = {'error': str(e)}
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup', 'enhanced-capability-analysis'),
                "function": event.get('function'),
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps(error_result)
                        }
                    }
                }
            },
            "sessionAttributes": {},
            "promptSessionAttributes": {}
        }

def get_internal_capabilities(query):
    query_lower = query.lower()
    all_skills = {
        'software_development': 85, 'hardware_engineering': 70, 'product_design': 90,
        'manufacturing': 60, 'supply_chain': 75, 'quality_assurance': 80,
        'regulatory_compliance': 65, 'marketing': 85, 'customer_support': 90,
        'data_analytics': 95, 'ai_ml': 80, 'iot_development': 70,
        'mobile_development': 85, 'cloud_infrastructure': 90
    }
    
    relevant_skills = {}
    if any(word in query_lower for word in ['smart', 'iot', 'connected']):
        relevant_skills.update({
            'iot_development': all_skills['iot_development'],
            'software_development': all_skills['software_development'],
            'hardware_engineering': all_skills['hardware_engineering'],
            'mobile_development': all_skills['mobile_development']
        })
    elif any(word in query_lower for word in ['app', 'software', 'digital']):
        relevant_skills.update({
            'software_development': all_skills['software_development'],
            'mobile_development': all_skills['mobile_development'],
            'cloud_infrastructure': all_skills['cloud_infrastructure'],
            'data_analytics': all_skills['data_analytics']
        })
    else:
        relevant_skills.update({
            'product_design': all_skills['product_design'],
            'manufacturing': all_skills['manufacturing'],
            'marketing': all_skills['marketing'],
            'supply_chain': all_skills['supply_chain']
        })
    
    avg_skill_level = sum(relevant_skills.values()) / len(relevant_skills) if relevant_skills else 50
    readiness = "High" if avg_skill_level >= 80 else "Medium" if avg_skill_level >= 65 else "Low"
    
    return {
        'relevant_skills': relevant_skills,
        'avg_skill_level': avg_skill_level,
        'readiness': readiness,
        'team_size': len(relevant_skills) * 3
    }

def get_supplier_capabilities(query):
    query_lower = query.lower()
    if any(word in query_lower for word in ['electronics', 'smart', 'device']):
        suppliers = {
            'electronics_manufacturing': {'capability': 85, 'cost': 'medium', 'lead_time': '8-12 weeks'},
            'component_sourcing': {'capability': 90, 'cost': 'low', 'lead_time': '4-6 weeks'},
            'pcb_assembly': {'capability': 80, 'cost': 'medium', 'lead_time': '6-8 weeks'}
        }
    else:
        suppliers = {
            'general_manufacturing': {'capability': 75, 'cost': 'medium', 'lead_time': '8-12 weeks'},
            'material_sourcing': {'capability': 80, 'cost': 'medium', 'lead_time': '4-6 weeks'}
        }
    
    avg_capability = sum(s['capability'] for s in suppliers.values()) / len(suppliers)
    readiness = "High" if avg_capability >= 85 else "Medium" if avg_capability >= 70 else "Low"
    
    return {
        'suppliers': suppliers,
        'avg_capability': avg_capability,
        'readiness': readiness,
        'supplier_count': len(suppliers)
    }

def analyze_capabilities(query, internal_data, supplier_data, required_skills):
    internal_skills = list(internal_data['relevant_skills'].keys())
    skill_matches = internal_skills[:4]
    
    query_lower = query.lower()
    potential_gaps = []
    if 'smart' in query_lower and 'ai_ml' not in internal_skills:
        potential_gaps.append('AI/ML expertise')
    if 'mobile' in query_lower and 'mobile_development' not in internal_skills:
        potential_gaps.append('Mobile app development')
    if 'hardware' in query_lower and 'hardware_engineering' not in internal_skills:
        potential_gaps.append('Hardware engineering')
    if 'manufacturing' not in internal_skills:
        potential_gaps.append('Manufacturing expertise')
    
    skill_gaps = potential_gaps[:3] if potential_gaps else ['Specialized domain knowledge']
    
    internal_readiness = internal_data['readiness']
    supplier_readiness = supplier_data['readiness']
    
    if internal_readiness == "High" and supplier_readiness == "High":
        time_to_market = "3-6 months"
        time_score = 90
    elif internal_readiness == "Medium" or supplier_readiness == "Medium":
        time_to_market = "6-12 months"
        time_score = 70
    else:
        time_to_market = "12-18 months"
        time_score = 50
    
    compliance_status = {
        'regulatory': 'Needs Assessment' if 'device' in query.lower() else 'Standard Review',
        'safety': 'Compliant',
        'environmental': 'Needs Review' if 'electronics' in query.lower() else 'Compliant',
        'data_privacy': 'Compliant' if 'smart' in query.lower() else 'Not Applicable'
    }
    
    risk_factors = []
    if internal_data['avg_skill_level'] < 70:
        risk_factors.append('Internal skill gaps')
    if supplier_data['avg_capability'] < 75:
        risk_factors.append('Supplier capability limitations')
    if len(skill_gaps) > 2:
        risk_factors.append('Multiple skill gaps to address')
    if 'smart' in query.lower():
        risk_factors.append('Technology complexity')
    
    recommended_actions = []
    if skill_gaps:
        recommended_actions.append(f"Acquire expertise in: {', '.join(skill_gaps[:2])}")
    if supplier_data['readiness'] != "High":
        recommended_actions.append("Strengthen supplier partnerships")
    if internal_data['team_size'] < 10:
        recommended_actions.append("Scale development team")
    recommended_actions.append("Conduct detailed feasibility study")
    
    internal_score = internal_data['avg_skill_level'] * 0.4
    supplier_score = supplier_data['avg_capability'] * 0.3
    time_score_weighted = time_score * 0.2
    risk_penalty = len(risk_factors) * 5
    
    capability_score = internal_score + supplier_score + time_score_weighted - risk_penalty
    capability_score = max(0, min(100, capability_score))
    
    return {
        'score': round(capability_score, 2),
        'skill_matches': skill_matches,
        'skill_gaps': skill_gaps,
        'internal_readiness': internal_readiness,
        'supplier_readiness': supplier_readiness,
        'time_to_market': time_to_market,
        'compliance_status': compliance_status,
        'recommended_actions': recommended_actions,
        'risk_factors': risk_factors
    }
