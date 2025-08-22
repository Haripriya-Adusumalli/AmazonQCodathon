import json

def lambda_handler(event, context):
    """Minimal working Lambda for Bedrock agent"""
    
    # Simple mock data
    result = {
        "demand_score": 75.0,
        "current_interest": 80.0,
        "momentum": 1.25,
        "trending_topics": ["smart water bottle reviews", "best smart water bottle", "smart water bottle price"],
        "news_volume": 45,
        "sentiment": "positive"
    }
    
    # Return simple JSON response
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }