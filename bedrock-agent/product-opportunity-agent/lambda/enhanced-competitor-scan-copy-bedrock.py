import json

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
