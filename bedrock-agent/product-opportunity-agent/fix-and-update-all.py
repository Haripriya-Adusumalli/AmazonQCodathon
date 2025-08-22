import boto3
import zipfile
import time

def fix_and_update_all_functions():
    """Fix market demand function and update all to use real APIs"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Fix market demand function first
    market_zip = "market-demand-fixed.zip"
    with zipfile.ZipFile(market_zip, 'w') as zip_file:
        zip_file.write("lambda/market-demand-real-api.py", "market-demand-function.py")
    
    with open(market_zip, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    print("Fixed market-demand-agent")
    time.sleep(5)
    
    # Update competitor scan to real API version
    competitor_zip = "competitor-scan-real.zip"
    with zipfile.ZipFile(competitor_zip, 'w') as zip_file:
        zip_file.write("lambda/competitor-scan-real-api.py", "competitor-scan-function.py")
    
    with open(competitor_zip, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='competitor-scan-agent',
            ZipFile=zip_file.read()
        )
    
    print("Updated competitor-scan-agent to real API version")
    
    print("All functions updated to use real API integration")

if __name__ == "__main__":
    fix_and_update_all_functions()