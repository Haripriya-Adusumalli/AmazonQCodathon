import json

def lambda_handler(event, context):
    """Market demand analysis with correct Bedrock response format"""
    
    try:
        # Parse Bedrock event
        api_path = event.get('apiPath', '/analyze-demand')
        http_method = event.get('httpMethod', 'POST')
        request_body = event.get('requestBody', {})
        
        # Extract query
        query = request_body.get('query', 'product')
        
        # Analysis
        result = {
            "demand_score": 75.0,
            "current_interest": 80.0,
            "momentum": 1.25,
            "trending_topics": [f"{query} reviews", f"best {query}", f"{query} price"],
            "news_volume": 45,
            "sentiment": "positive"
        }
        
        # Bedrock-compatible response
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup', 'market-demand'),
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
                "actionGroup": event.get('actionGroup', 'market-demand'),
                "apiPath": event.get('apiPath', '/analyze-demand'),
                "httpMethod": event.get('httpMethod', 'POST'),
                "httpStatusCode": 500,
                "responseBody": {
                    "application/json": {
                        "body": json.dumps({"error": str(e)})
                    }
                }
            }
        }