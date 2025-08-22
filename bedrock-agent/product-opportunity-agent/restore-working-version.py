import boto3
import zipfile

def restore_working_version():
    """Restore the working mock version"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    with zipfile.ZipFile("market-demand-working.zip", 'w') as zip_file:
        zip_file.write("lambda/market-demand-simple.py", "market-demand-function.py")
    
    with open("market-demand-working.zip", 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    print("Restored working mock version")

if __name__ == "__main__":
    restore_working_version()