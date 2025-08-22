import boto3
import zipfile

def fix_market_demand_lambda():
    """Fix the market demand Lambda function"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Create new deployment package with correct structure
    zip_path = "market-demand-fixed.zip"
    
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        zip_file.write("lambda/market-demand-function.py", "market-demand-function.py")
    
    # Update function code
    with open(zip_path, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    print("Fixed market-demand-agent Lambda function")

if __name__ == "__main__":
    fix_market_demand_lambda()