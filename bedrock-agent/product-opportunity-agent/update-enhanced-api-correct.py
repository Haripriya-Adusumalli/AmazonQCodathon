import boto3
import zipfile

def update_enhanced_api_correct():
    """Update enhanced function with API calls and correct format"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    with zipfile.ZipFile("enhanced-api-correct.zip", 'w') as zip_file:
        zip_file.write("lambda/enhanced-market-demand-api-correct.py", "lambda_function.py")
    
    with open("enhanced-api-correct.zip", 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='enhanced-market-demand-copy',
            ZipFile=zip_file.read()
        )
    
    print("Updated enhanced function with API calls and correct Bedrock format")

if __name__ == "__main__":
    update_enhanced_api_correct()