import boto3
import zipfile
import json

def restore_working_lambda():
    """Restore the working Lambda function with Bedrock input format handling"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # The working code with Bedrock input format handling
    working_code = '''import json
import requests
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """Market Demand Agent - analyzes demand signals"""
    
    try:
        # Handle Bedrock agent input format
        if 'inputText' in event:
            query = event['inputText']
            region = 'US'
        elif 'parameters' in event:
            params = event['parameters']
            query = params.get('query', '')
            region = params.get('region', 'US')
        else:
            query = event.get('query', '')
            region = event.get('region', 'US')
        
        # Mock Google Trends data (replace with actual pytrends in production)
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
'''
    
    # Write working code to file
    with open('lambda/market-demand-function.py', 'w') as f:
        f.write(working_code)
    
    # Create zip and update function
    zip_filename = 'market-demand-working.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        zip_file.write('lambda/market-demand-function.py', 'lambda_function.py')
    
    with open(zip_filename, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    print("Restored market-demand-agent to working version with Bedrock input handling")

if __name__ == "__main__":
    restore_working_lambda()