import json

def lambda_handler(event, context):
    """Simple market demand function"""
    try:
        # Get query from event
        query = event.get('inputText', event.get('query', 'product'))
        
        # Simple calculations
        base_score = len(query) * 3
        current_interest = min(100, base_score + abs(hash(query)) % 30)
        momentum = 1.0 + (abs(hash(query)) % 50) / 100
        demand_score = min(100, current_interest * 0.8)
        
        result = {
            'demand_score': round(demand_score, 2),
            'current_interest': round(current_interest, 2),
            'momentum': round(momentum, 2),
            'trending_topics': [f"{query} reviews", f"best {query}", f"{query} 2024"],
            'news_volume': min(50, len(query) * 2),
            'region': 'US'
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
