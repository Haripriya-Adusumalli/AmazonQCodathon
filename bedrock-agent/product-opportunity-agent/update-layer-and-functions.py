import boto3
import subprocess
import zipfile
import os

def update_layer_and_functions():
    """Update Lambda layer with pytrends and update functions with real API code"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Create enhanced layer with pytrends
    layer_dir = "lambda-layer-enhanced"
    python_dir = f"{layer_dir}/python"
    
    os.makedirs(python_dir, exist_ok=True)
    
    # Install dependencies
    subprocess.run([
        "pip", "install", "requests", "pytrends", "-t", python_dir
    ], check=True)
    
    # Create layer zip
    layer_zip = "enhanced-layer.zip"
    with zipfile.ZipFile(layer_zip, 'w') as zip_file:
        for root, dirs, files in os.walk(layer_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, layer_dir)
                zip_file.write(file_path, arc_path)
    
    # Publish new layer version
    with open(layer_zip, 'rb') as zip_file:
        layer_response = lambda_client.publish_layer_version(
            LayerName='requests-layer',
            Description='Enhanced layer with requests and pytrends',
            Content={'ZipFile': zip_file.read()},
            CompatibleRuntimes=['python3.9']
        )
    
    layer_arn = layer_response['LayerVersionArn']
    print(f"Created enhanced layer: {layer_arn}")
    
    # Update market demand function with real API code
    market_zip = "market-demand-real.zip"
    with zipfile.ZipFile(market_zip, 'w') as zip_file:
        zip_file.write("lambda/market-demand-real-api.py", "market-demand-real-api.py")
    
    with open(market_zip, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='market-demand-agent',
            ZipFile=zip_file.read()
        )
    
    # Update handler and layer
    lambda_client.update_function_configuration(
        FunctionName='market-demand-agent',
        Handler='market-demand-real-api.lambda_handler',
        Layers=[layer_arn],
        Environment={
            'Variables': {
                'NEWS_API_KEY': 'your_news_api_key_here',
                'AMAZON_ACCESS_KEY': 'your_amazon_access_key',
                'AMAZON_SECRET_KEY': 'your_amazon_secret_key',
                'AMAZON_PARTNER_TAG': 'your_partner_tag'
            }
        }
    )
    
    # Update competitor scan function
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
        Handler='competitor-scan-real-api.lambda_handler',
        Layers=[layer_arn],
        Environment={
            'Variables': {
                'EBAY_APP_ID': 'your_ebay_app_id',
                'AMAZON_ACCESS_KEY': 'your_amazon_access_key',
                'AMAZON_SECRET_KEY': 'your_amazon_secret_key'
            }
        }
    )
    
    print("Updated Lambda functions with real API integration")
    print("Note: Add your actual API keys to the environment variables")

if __name__ == "__main__":
    update_layer_and_functions()