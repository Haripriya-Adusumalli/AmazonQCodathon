import boto3
import zipfile

def update_simple_correct():
    """Update to simple correct format"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    with zipfile.ZipFile("enhanced-simple-correct.zip", 'w') as zip_file:
        zip_file.write("lambda/enhanced-market-demand-simple-correct.py", "lambda_function.py")
    
    with open("enhanced-simple-correct.zip", 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='enhanced-market-demand-copy',
            ZipFile=zip_file.read()
        )
    
    print("Updated to simple correct format")

if __name__ == "__main__":
    update_simple_correct()