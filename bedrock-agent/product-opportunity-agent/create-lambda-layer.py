import boto3
import os
import zipfile
import subprocess

def create_requests_layer():
    """Create Lambda layer with requests library"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Create layer directory structure
    layer_dir = "lambda-layer"
    python_dir = f"{layer_dir}/python"
    
    os.makedirs(python_dir, exist_ok=True)
    
    # Install requests to layer directory
    subprocess.run([
        "pip", "install", "requests", "-t", python_dir
    ], check=True)
    
    # Create layer zip
    layer_zip = "requests-layer.zip"
    with zipfile.ZipFile(layer_zip, 'w') as zip_file:
        for root, dirs, files in os.walk(layer_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, layer_dir)
                zip_file.write(file_path, arc_path)
    
    # Upload layer
    with open(layer_zip, 'rb') as zip_file:
        response = lambda_client.publish_layer_version(
            LayerName='requests-layer',
            Description='Requests library for Lambda functions',
            Content={'ZipFile': zip_file.read()},
            CompatibleRuntimes=['python3.9']
        )
    
    layer_arn = response['LayerVersionArn']
    print(f"Created layer: {layer_arn}")
    
    # Update market-demand-agent with layer
    lambda_client.update_function_configuration(
        FunctionName='market-demand-agent',
        Layers=[layer_arn]
    )
    
    print("Updated market-demand-agent with requests layer")
    return layer_arn

if __name__ == "__main__":
    create_requests_layer()