import boto3
import zipfile

def update_lambdas_to_real_apis():
    """Update Lambda functions to use real APIs instead of mock data"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Update market demand function with real API code
    market_zip = "market-demand-real.zip"
    with zipfile.ZipFile(market_zip, 'w') as zip_file:
        zip_file.write("lambda/market-demand-real-api.py", "market-demand-real-api.py")
    
    with open(market_zip, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    lambda_client.update_function_configuration(
        FunctionName='market-demand-agent',
        Handler='market-demand-real-api.lambda_handler'
    )
    
    # Update competitor scan function with real API code
    competitor_zip = "competitor-scan-real.zip"
    with zipfile.ZipFile(competitor_zip, 'w') as zip_file:
        zip_file.write("lambda/competitor-scan-real-api.py", "competitor-scan-real-api.py")
    
    with open(competitor_zip, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='competitor-scan-agent',
            ZipFile=zip_file.read()
        )
    
    lambda_client.update_function_configuration(
        FunctionName='competitor-scan-agent',
        Handler='competitor-scan-real-api.lambda_handler'
    )
    
    print("Updated Lambda functions to use real API code")
    print("Note: Functions will use mock data if API keys are not provided")

if __name__ == "__main__":
    update_lambdas_to_real_apis()