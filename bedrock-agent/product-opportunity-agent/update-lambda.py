import boto3
import zipfile
import json

def update_market_demand_lambda():
    """Update the market demand Lambda function"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Create new deployment package
    zip_path = "lambda/market-demand-function-fixed.zip"
    
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        zip_file.write("lambda/market-demand-function-fixed.py", "market-demand-function-fixed.py")
    
    # Update function code
    with open(zip_path, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    # Update handler
    lambda_client.update_function_configuration(
        FunctionName='market-demand-agent',
        Handler='market-demand-function-fixed.lambda_handler'
    )
    
    print("Updated market-demand-agent Lambda function")

if __name__ == "__main__":
    update_market_demand_lambda()