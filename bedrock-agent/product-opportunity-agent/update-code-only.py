import boto3
import zipfile

def update_code_only():
    """Update Lambda function code only"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Update market demand
    with zipfile.ZipFile("market-demand-bedrock.zip", 'w') as zip_file:
        zip_file.write("lambda/market-demand-bedrock-format.py", "market-demand-function.py")
    
    with open("market-demand-bedrock.zip", 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    print("Updated market-demand-agent")

if __name__ == "__main__":
    update_code_only()