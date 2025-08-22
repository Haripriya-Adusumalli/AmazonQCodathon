import boto3
import zipfile

def update_code_only_enhanced():
    """Update enhanced function code only"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    with zipfile.ZipFile("enhanced-market-demand-real.zip", 'w') as zip_file:
        zip_file.write("lambda/enhanced-market-demand-real-api.py", "lambda_function.py")
    
    with open("enhanced-market-demand-real.zip", 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='enhanced-market-demand-copy',
            ZipFile=zip_file.read()
        )
    
    print("Updated enhanced-market-demand-copy with real API integration")

if __name__ == "__main__":
    update_code_only_enhanced()