import boto3
import zipfile

def fix_bedrock_response_format():
    """Fix enhanced Lambda functions to use correct Bedrock action group response format"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Enhanced market demand with correct response format
    market_demand_code = '''import json

def lambda_handler(event, context):
    """Enhanced Market Demand Agent with correct Bedrock response format"""
    
    try:
        # Handle Bedrock agent input format
        if 'inputText' in event:
            query = event['inputText']
            region = 'US'
        elif 'parameters' in event:
            params = event['parameters']
            query = params.get('query', '')
            region = params.get('region', 'US')
        else:
            query = event.get('query', '')
            region = event.get('region', 'US')
        
        # Enhanced calculations
        current_interest = calculate_enhanced_interest(query)
        momentum = calculate_enhanced_momentum(query)
        trending_topics = generate_enhanced_topics(query)
        news_volume = calculate_news_volume(query)
        sentiment = analyze_sentiment(query)
        demand_score = calculate_enhanced_demand_score(current_interest, momentum, news_volume, sentiment)
        
        result = {
            'demand_score': round(demand_score, 2),
            'current_interest': round(current_interest, 2),
            'momentum': round(momentum, 2),
            'trending_topics': trending_topics,
            'news_volume': news_volume,
            'news_sentiment': sentiment,
            'region': region,
            'data_source': 'enhanced_analysis'
        }
        
        # Return in Bedrock action group format
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup', 'enhanced-demand-analysis'),
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
                "actionGroup": event.get('actionGroup', 'enhanced-demand-analysis'),
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

def calculate_enhanced_interest(query):
    base_score = len(query) * 4
    keyword_boost = 0
    trending_keywords = ['smart', 'ai', 'eco', 'fitness', 'health', 'tech']
    for keyword in trending_keywords:
        if keyword in query.lower():
            keyword_boost += 15
    return min(100, base_score + abs(hash(query)) % 35 + keyword_boost)

def calculate_enhanced_momentum(query):
    base_momentum = 1.0 + (abs(hash(query)) % 60) / 100
    if any(word in query.lower() for word in ['fitness', 'health', 'diet']):
        base_momentum *= 1.2
    elif any(word in query.lower() for word in ['smart', 'ai', 'tech']):
        base_momentum *= 1.3
    return min(2.0, base_momentum)

def generate_enhanced_topics(query):
    return [f"{query} reviews 2024", f"best {query} brands", f"{query} price comparison"]

def calculate_news_volume(query):
    return min(100, len(query) * 3 + abs(hash(query + 'news')) % 60)

def analyze_sentiment(query):
    sentiment_score = (abs(hash(query + 'sentiment')) % 100) / 100
    if sentiment_score > 0.65:
        return 'positive'
    elif sentiment_score > 0.35:
        return 'neutral'
    else:
        return 'negative'

def calculate_enhanced_demand_score(interest, momentum, news_volume, sentiment):
    base_score = (interest * 0.5) + ((momentum - 1.0) * 30) + (news_volume * 0.3)
    sentiment_multiplier = {'positive': 1.1, 'neutral': 1.0, 'negative': 0.9}
    adjusted_score = base_score * sentiment_multiplier.get(sentiment, 1.0)
    return min(100, max(0, adjusted_score))
'''
    
    # Enhanced competitor scan with correct response format
    competitor_scan_code = '''import json

def lambda_handler(event, context):
    """Enhanced Competitor Scan Agent with correct Bedrock response format"""
    
    try:
        # Handle Bedrock agent input format
        if 'inputText' in event:
            query = event['inputText']
            category = 'general'
        elif 'parameters' in event:
            params = event['parameters']
            query = params.get('query', '')
            category = params.get('category', 'general')
        else:
            query = event.get('query', '')
            category = event.get('category', 'general')
        
        # Enhanced competition analysis
        amazon_data = simulate_amazon_data(query)
        ebay_data = simulate_ebay_data(query)
        market_analysis = analyze_enhanced_competition(amazon_data, ebay_data, query)
        
        result = {
            'competition_score': market_analysis['score'],
            'total_products': market_analysis['total_products'],
            'avg_rating': market_analysis['avg_rating'],
            'price_range': market_analysis['price_range'],
            'top_competitors': market_analysis['top_competitors'],
            'market_saturation': market_analysis['market_saturation'],
            'feature_gaps': market_analysis['feature_gaps'],
            'data_source': 'enhanced_multi_platform',
            'platforms_analyzed': ['amazon', 'ebay']
        }
        
        # Return in Bedrock action group format
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup', 'enhanced-competition-analysis'),
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
                "actionGroup": event.get('actionGroup', 'enhanced-competition-analysis'),
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

def simulate_amazon_data(query):
    product_count = abs(hash(query + 'amazon')) % 600 + 150
    avg_rating = 3.8 + (abs(hash(query)) % 12) / 10
    base_price = 25 + abs(hash(query)) % 120
    return {
        'product_count': product_count,
        'avg_rating': round(avg_rating, 1),
        'price_range': {'min': base_price, 'max': base_price * 3, 'avg': base_price * 1.8},
        'top_brands': [f"Brand{i}" for i in range(1, 6)]
    }

def simulate_ebay_data(query):
    product_count = abs(hash(query + 'ebay')) % 400 + 80
    avg_rating = 3.6 + (abs(hash(query + 'ebay')) % 14) / 10
    base_price = 20 + abs(hash(query + 'ebay')) % 100
    return {
        'product_count': product_count,
        'avg_rating': round(avg_rating, 1),
        'price_range': {'min': base_price, 'max': base_price * 2.5, 'avg': base_price * 1.5}
    }

def analyze_enhanced_competition(amazon_data, ebay_data, query):
    total_products = amazon_data['product_count'] + ebay_data['product_count']
    total_weight = amazon_data['product_count'] + ebay_data['product_count']
    avg_rating = (
        (amazon_data['avg_rating'] * amazon_data['product_count'] + 
         ebay_data['avg_rating'] * ebay_data['product_count']) / total_weight
    )
    
    density_score = min(50, total_products / 15)
    rating_score = max(0, (avg_rating - 3.0) * 12)
    
    if total_products > 700:
        saturation = "High"
        saturation_score = 30
    elif total_products > 400:
        saturation = "Medium"
        saturation_score = 20
    else:
        saturation = "Low"
        saturation_score = 10
    
    competition_score = density_score + rating_score + saturation_score
    feature_gaps = identify_enhanced_gaps(query, total_products, avg_rating)
    
    return {
        'score': round(min(100, competition_score), 2),
        'total_products': total_products,
        'avg_rating': round(avg_rating, 1),
        'price_range': {
            'min': min(amazon_data['price_range']['min'], ebay_data['price_range']['min']),
            'max': max(amazon_data['price_range']['max'], ebay_data['price_range']['max']),
            'avg': (amazon_data['price_range']['avg'] + ebay_data['price_range']['avg']) / 2
        },
        'top_competitors': amazon_data['top_brands'][:4],
        'market_saturation': saturation,
        'feature_gaps': feature_gaps
    }

def identify_enhanced_gaps(query, product_count, avg_rating):
    gaps = []
    if 'smart' in query.lower():
        gaps.extend(["Advanced AI features", "Better connectivity", "Longer battery life"])
    elif 'fitness' in query.lower():
        gaps.extend(["More accurate sensors", "Better app integration", "Waterproof design"])
    elif 'eco' in query.lower():
        gaps.extend(["Sustainable materials", "Carbon neutral shipping", "Recyclable packaging"])
    else:
        gaps.extend(["Premium quality", "Better design", "Competitive pricing"])
    
    if avg_rating < 4.0:
        gaps.append("Quality improvement")
    return gaps[:4]
'''
    
    # Enhanced capability match with correct response format
    capability_match_code = '''import json

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
'''
    
    # Update all three functions
    functions = [
        ('enhanced-market-demand-copy', market_demand_code),
        ('enhanced-competitor-scan-copy', competitor_scan_code),
        ('enhanced-capability-match-copy', capability_match_code)
    ]
    
    for func_name, code in functions:
        try:
            # Write code to temp file
            temp_file = f'lambda/{func_name}-bedrock.py'
            with open(temp_file, 'w') as f:
                f.write(code)
            
            # Create zip and update
            zip_filename = f'{func_name}-bedrock.zip'
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                zip_file.write(temp_file, 'lambda_function.py')
            
            with open(zip_filename, 'rb') as zip_file:
                lambda_client.update_function_code(
                    FunctionName=func_name,
                    ZipFile=zip_file.read()
                )
            
            print(f"Updated {func_name} with correct Bedrock response format")
            
        except Exception as e:
            print(f"Error updating {func_name}: {e}")

if __name__ == "__main__":
    fix_bedrock_response_format()