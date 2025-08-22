import json

def lambda_handler(event, context):
    """Capability match with correct Bedrock response format"""
    
    try:
        api_path = event.get('apiPath', '/analyze-capability')
        http_method = event.get('httpMethod', 'POST')
        request_body = event.get('requestBody', {})
        
        query = request_body.get('query', 'product')
        
        result = {
            "capability_score": 70.0,
            "skill_matches": ["product design", "marketing", "supply chain"],
            "skill_gaps": ["specialized expertise"],
            "supplier_readiness": "Medium",
            "time_to_market": "4-8 months",
            "compliance_status": {
                "regulatory": "Needs Review",
                "safety": "Compliant",
                "environmental": "Compliant"
            },
            "recommended_actions": [
                "Hire expertise in specialized areas",
                "Evaluate supplier partnerships",
                "Conduct market validation study"
            ]
        }
        
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get('actionGroup', 'capability-match'),
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
                "actionGroup": event.get('actionGroup', 'capability-match'),
                "apiPath": event.get('apiPath', '/analyze-capability'),
                "httpMethod": event.get('httpMethod', 'POST'),
                "httpStatusCode": 500,
                "responseBody": {
                    "application/json": {
                        "body": json.dumps({"error": str(e)})
                    }
                }
            }
        }