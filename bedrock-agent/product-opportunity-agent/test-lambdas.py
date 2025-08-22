import boto3
import json

def test_lambda_functions():
    """Test all deployed Lambda functions"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    functions = [
        'market-demand-agent',
        'competitor-scan-agent', 
        'capability-match-agent'
    ]
    
    test_payload = {
        'query': 'smart water bottle',
        'region': 'US'
    }
    
    for function_name in functions:
        try:
            print(f"\nTesting {function_name}...")
            
            response = lambda_client.invoke(
                FunctionName=function_name,
                Payload=json.dumps(test_payload)
            )
            
            result = json.loads(response['Payload'].read())
            print(f"Status: {result.get('statusCode', 'Unknown')}")
            
            if result.get('statusCode') == 200:
                body = json.loads(result.get('body', '{}'))
                print(f"Response: {json.dumps(body, indent=2)}")
            else:
                print(f"Error: {result}")
                
        except Exception as e:
            print(f"Error testing {function_name}: {e}")

if __name__ == "__main__":
    test_lambda_functions()