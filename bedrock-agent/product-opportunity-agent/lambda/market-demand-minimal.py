import json

def lambda_handler(event, context):
    """Minimal working Bedrock response"""
    
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": "market-demand",
            "apiPath": "/analyze-demand", 
            "httpMethod": "POST",
            "httpStatusCode": 200,
            "responseBody": {
                "application/json": {
                    "body": json.dumps({
                        "demand_score": 75.0,
                        "current_interest": 80.0,
                        "momentum": 1.25,
                        "trending_topics": ["smart water bottle reviews", "best smart water bottle", "smart water bottle price"],
                        "news_volume": 45,
                        "sentiment": "positive"
                    })
                }
            }
        }
    }