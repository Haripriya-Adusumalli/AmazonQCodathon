import boto3
import zipfile

def update_minimal_enhanced():
    """Update enhanced function to minimal working version"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    with zipfile.ZipFile("enhanced-minimal.zip", 'w') as zip_file:
        zip_file.write("lambda/enhanced-market-demand-minimal.py", "lambda_function.py")
    
    with open("enhanced-minimal.zip", 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='enhanced-market-demand-copy',
            ZipFile=zip_file.read()
        )
    
    print("Updated to minimal working version")

if __name__ == "__main__":
    update_minimal_enhanced()