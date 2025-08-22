import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """Market Demand Agent - analyzes demand signals"""
    
    try:
        query = event.get('query', '')
        region = event.get('region', 'US')
        
        # Mock demand analysis (no external dependencies)
        current_interest = calculate_mock_interest(query)
        momentum = calculate_mock_momentum(query)
        trending_topics = generate_mock_topics(query)
        
        # Mock news volume
        news_volume = min(50, len(query) * 2)
        
        # Calculate demand score (0-100)
        demand_score = min(100, (current_interest * 0.6 + momentum * 20 + news_volume * 0.2))
        
        result = {
            'demand_score': round(demand_score, 2),
            'current_interest': round(current_interest, 2),
            'momentum': round(momentum, 2),
            'trending_topics': trending_topics,
            'news_volume': news_volume,
            'region': region,
            'analysis_type': 'mock_data'
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

def calculate_mock_interest(query):
    """Mock interest calculation"""
    base_score = len(query) * 3
    return min(100, base_score + hash(query) % 30)

def calculate_mock_momentum(query):
    """Mock momentum calculation"""
    return 1.0 + (hash(query) % 50) / 100

def generate_mock_topics(query):
    """Generate mock trending topics"""
    topics = [
        f"{query} reviews",
        f"best {query}",
        f"{query} alternatives",
        f"cheap {query}",
        f"{query} 2024"
    ]
    return topics[:3]