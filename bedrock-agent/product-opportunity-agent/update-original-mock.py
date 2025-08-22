import boto3
import zipfile

def update_original_mock():
    """Update to original mock version with Bedrock compatibility"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    with zipfile.ZipFile("market-demand-original.zip", 'w') as zip_file:
        zip_file.write("lambda/market-demand-original-mock.py", "market-demand-function.py")
    
    with open("market-demand-original.zip", 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    print("Updated to original mock version with Bedrock compatibility")

if __name__ == "__main__":
    update_original_mock()