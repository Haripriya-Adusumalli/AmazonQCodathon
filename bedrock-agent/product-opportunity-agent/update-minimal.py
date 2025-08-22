import boto3
import zipfile

def update_minimal():
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    with zipfile.ZipFile("market-demand-minimal.zip", 'w') as zip_file:
        zip_file.write("lambda/market-demand-minimal.py", "market-demand-function.py")
    
    with open("market-demand-minimal.zip", 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    print("Updated to minimal format")

if __name__ == "__main__":
    update_minimal()