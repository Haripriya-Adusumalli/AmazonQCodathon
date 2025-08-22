import json

def lambda_handler(event, context):
    """Market Demand Agent - analyzes demand signals with original mock data"""
    
    try:
        # Extract query from different event formats
        query = 'product'
        if 'requestBody' in event and event['requestBody']:
            query = event['requestBody'].get('query', 'product')
        elif 'query' in event:
            query = event['query']
        elif 'inputText' in event:
            query = event['inputText']
        
        region = 'US'
        if 'requestBody' in event and event['requestBody']:
            region = event['requestBody'].get('region', 'US')
        elif 'region' in event:
            region = event['region']
        
        # Original mock calculations
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
            'region': region
        }
        
        # Try Bedrock format first, fallback to simple format
        if 'actionGroup' in event:
            return {
                "messageVersion": "1.0",
                "response": {
                    "actionGroup": event.get('actionGroup', 'market-demand'),
                    "apiPath": event.get('apiPath', '/analyze-demand'),
                    "httpMethod": event.get('httpMethod', 'POST'),
                    "httpStatusCode": 200,
                    "responseBody": {
                        "application/json": {
                            "body": json.dumps(result)
                        }
                    }
                }
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        
    except Exception as e:
        error_result = {'error': str(e)}
        
        if 'actionGroup' in event:
            return {
                "messageVersion": "1.0",
                "response": {
                    "actionGroup": event.get('actionGroup', 'market-demand'),
                    "apiPath": event.get('apiPath', '/analyze-demand'),
                    "httpMethod": event.get('httpMethod', 'POST'),
                    "httpStatusCode": 500,
                    "responseBody": {
                        "application/json": {
                            "body": json.dumps(error_result)
                        }
                    }
                }
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps(error_result)
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