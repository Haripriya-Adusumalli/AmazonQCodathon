import json
from datetime import datetime

def lambda_handler(event, context):
    """Simple enhanced market demand with correct format"""
    
    try:
        # Extract query
        query = 'product'
        if 'requestBody' in event and event['requestBody']:
            if isinstance(event['requestBody'], str):
                body = json.loads(event['requestBody'])
            else:
                body = event['requestBody']
            query = body.get('query', 'product')
        
        # Enhanced mock analysis with API simulation
        trends_data = get_enhanced_trends(query)
        news_data = get_enhanced_news(query)
        demand_score = calculate_demand_score(trends_data, news_data)
        
        result = {
            'demand_score': round(demand_score, 2),
            'current_interest': trends_data['current_interest'],
            'momentum': trends_data['momentum'],
            'trending_topics': trends_data['trending_topics'],
            'news_volume': news_data['volume'],
            'news_sentiment': news_data['sentiment'],
            'data_source': 'enhanced_mock',
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Return simple JSON (let Bedrock handle the formatting)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_enhanced_trends(query):
    """Enhanced trends analysis"""
    query_lower = query.lower()
    
    # Smart categorization
    if any(word in query_lower for word in ['smart', 'ai', 'iot']):
        base_interest = 85
        category = "smart_tech"
    elif any(word in query_lower for word in ['eco', 'green', 'sustainable']):
        base_interest = 78
        category = "eco_friendly"
    elif any(word in query_lower for word in ['fitness', 'health', 'wellness']):
        base_interest = 82
        category = "health_fitness"
    else:
        base_interest = 65
        category = "general"
    
    current_interest = min(100, base_interest + (hash(query) % 15))
    momentum = 1.1 + (hash(query + category) % 30) / 100
    
    # Category-specific trending topics
    if category == "smart_tech":
        trending_topics = [f"smart {query} reviews", f"IoT {query} features", f"{query} connectivity"]
    elif category == "eco_friendly":
        trending_topics = [f"sustainable {query}", f"eco-friendly {query}", f"green {query} options"]
    elif category == "health_fitness":
        trending_topics = [f"{query} health benefits", f"fitness {query}", f"{query} wellness"]
    else:
        trending_topics = [f"{query} reviews", f"best {query} 2024", f"{query} comparison"]
    
    return {
        'current_interest': round(current_interest, 2),
        'momentum': round(momentum, 2),
        'trending_topics': trending_topics[:3]
    }

def get_enhanced_news(query):
    """Enhanced news analysis"""
    volume = len(query) * 4
    
    # Category-based adjustments
    if any(word in query.lower() for word in ['smart', 'ai', 'tech']):
        volume += 20
        sentiment = 'positive'
    elif any(word in query.lower() for word in ['eco', 'green', 'sustainable']):
        volume += 18
        sentiment = 'positive'
    elif any(word in query.lower() for word in ['health', 'fitness']):
        volume += 15
        sentiment = 'positive'
    else:
        sentiment = 'neutral'
    
    return {
        'volume': min(100, volume),
        'sentiment': sentiment
    }

def calculate_demand_score(trends_data, news_data):
    """Calculate demand score"""
    interest_score = trends_data['current_interest']
    momentum_score = trends_data['momentum'] * 25
    news_score = news_data['volume'] * 0.3
    
    sentiment_bonus = 10 if news_data['sentiment'] == 'positive' else 0
    
    total_score = interest_score * 0.5 + momentum_score * 0.3 + news_score * 0.2 + sentiment_bonus
    return max(0, min(100, total_score))