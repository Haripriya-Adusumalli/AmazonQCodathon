import boto3
import zipfile

def update_to_hybrid_functions():
    """Update functions to hybrid versions with enhanced mock fallback"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Update market demand to hybrid version
    market_zip = "market-demand-hybrid.zip"
    with zipfile.ZipFile(market_zip, 'w') as zip_file:
        zip_file.write("lambda/market-demand-hybrid.py", "market-demand-function.py")
    
    with open(market_zip, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    # Update competitor scan to use enhanced mock
    competitor_zip = "competitor-scan-enhanced.zip"
    with zipfile.ZipFile(competitor_zip, 'w') as zip_file:
        zip_file.write("lambda/competitor-scan-real-api.py", "competitor-scan-function.py")
    
    with open(competitor_zip, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='competitor-scan-agent',
            ZipFile=zip_file.read()
        )
    
    print("Updated functions to hybrid versions with enhanced analysis")

if __name__ == "__main__":
    update_to_hybrid_functions()