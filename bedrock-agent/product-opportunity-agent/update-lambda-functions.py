import boto3
import zipfile
import os

def update_lambda_functions():
    """Update all Lambda functions with Bedrock-compatible input handling"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    functions = [
        'market-demand-agent',
        'competitor-scan-agent', 
        'capability-match-agent'
    ]
    
    for func_name in functions:
        try:
            # Create zip file
            zip_filename = f"{func_name}.zip"
            py_filename = f"lambda/{func_name.replace('-agent', '-function')}.py"
            
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                zip_file.write(py_filename, 'lambda_function.py')
            
            # Update function code
            with open(zip_filename, 'rb') as zip_file:
                lambda_client.update_function_code(
                    FunctionName=func_name,
                    ZipFile=zip_file.read()
                )
            
            print(f"Updated {func_name}")
            
            # Clean up
            os.remove(zip_filename)
            
        except Exception as e:
            print(f"Error updating {func_name}: {e}")

if __name__ == "__main__":
    update_lambda_functions()