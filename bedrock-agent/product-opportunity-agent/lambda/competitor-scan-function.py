import json

def lambda_handler(event, context):
    """Simple competitor scan function"""
    try:
        query = event.get('query', event.get('inputText', 'product'))
        
        # Simple mock data
        total_products = abs(hash(query)) % 500 + 100
        avg_rating = 3.5 + (hash(query) % 15) / 10
        
        result = {
            'competition_score': min(100, total_products / 10 + avg_rating * 5),
            'total_products': total_products,
            'avg_rating': round(avg_rating, 1),
            'price_range': {'low': 25, 'high': 150},
            'top_competitors': ['CompetitorA', 'CompetitorB'],
            'market_saturation': 'Medium',
            'feature_gaps': ['Better design', 'Lower price']
        }
        
        return {'statusCode': 200, 'body': json.dumps(result)}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
