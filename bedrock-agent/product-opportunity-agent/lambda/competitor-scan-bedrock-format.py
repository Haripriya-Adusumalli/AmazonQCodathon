import json

def lambda_handler(event, context):
    """Competitor scan with correct Bedrock response format"""
    
    try:
        api_path = event.get('apiPath', '/analyze-competition')
        http_method = event.get('httpMethod', 'POST')
        request_body = event.get('requestBody', {})
        
        query = request_body.get('query', 'product')
        
        result = {
            "competition_score": 45.0,
            "total_products": 150,
            "avg_rating": 4.2,
            "price_range": {"low": 25, "high": 85},
            "top_competitors": ["Brand1", "Brand2", "Brand3"],
            "market_saturation": "Medium",
            "feature_gaps": ["Better battery life", "Improved design", "Lower price point"]
        }
        
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup', 'competition-scan'),
                "apiPath": api_path,
                "httpMethod": http_method,
                "httpStatusCode": 200,
                "responseBody": {
                    "application/json": {
                        "body": json.dumps(result)
                    }
                }
            }
        }
        
    except Exception as e:
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup', 'competition-scan'),
                "apiPath": event.get('apiPath', '/analyze-competition'),
                "httpMethod": event.get('httpMethod', 'POST'),
                "httpStatusCode": 500,
                "responseBody": {
                    "application/json": {
                        "body": json.dumps({"error": str(e)})
                    }
                }
            }
        }