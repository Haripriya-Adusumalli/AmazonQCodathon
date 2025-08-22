import boto3
import json

def test_enhanced_lambdas():
    """Test the enhanced Lambda functions directly"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Test data
    test_event = {
        'inputText': 'smart fitness tracker',
        'query': 'smart fitness tracker',
        'region': 'US'
    }
    
    functions = [
        'enhanced-market-demand-copy',
        'enhanced-competitor-scan-copy', 
        'enhanced-capability-match-copy'
    ]
    
    for func_name in functions:
        try:
            print(f"\\nTesting {func_name}...")
            
            response = lambda_client.invoke(
                FunctionName=func_name,
                Payload=json.dumps(test_event)
            )
            
            result = json.loads(response['Payload'].read())
            print(f"Status: {result.get('statusCode', 'Unknown')}")
            
            if result.get('statusCode') == 200:
                body = json.loads(result['body'])
                print(f"Success! Sample data: {list(body.keys())}")
            else:
                print(f"Error: {result.get('body', 'Unknown error')}")
                
        except Exception as e:
            print(f"Failed to test {func_name}: {e}")

if __name__ == "__main__":
    test_enhanced_lambdas()