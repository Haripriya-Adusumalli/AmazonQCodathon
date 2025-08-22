import boto3
import zipfile

def update_simple():
    """Update to simple Lambda function"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Update market demand function
    market_zip = "market-demand-simple.zip"
    with zipfile.ZipFile(market_zip, 'w') as zip_file:
        zip_file.write("lambda/market-demand-simple.py", "market-demand-function.py")
    
    with open(market_zip, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    print("Updated to simple format")

if __name__ == "__main__":
    update_simple()