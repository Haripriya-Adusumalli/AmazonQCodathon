import boto3
import zipfile

def update_all_bedrock_format():
    """Update all Lambda functions to correct Bedrock format"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    functions = [
        ('market-demand-agent', 'market-demand-bedrock-format.py'),
        ('competitor-scan-agent', 'competitor-scan-bedrock-format.py'),
        ('capability-match-agent', 'capability-match-bedrock-format.py')
    ]
    
    for func_name, file_name in functions:
        zip_name = f"{func_name}-bedrock.zip"
        
        with zipfile.ZipFile(zip_name, 'w') as zip_file:
            zip_file.write(f"lambda/{file_name}", f"{func_name.replace('-', '_')}_function.py")
        
        with open(zip_name, 'rb') as zip_file:
            lambda_client.update_function_code(
                FunctionName=func_name,
                ZipFile=zip_file.read()
            )
        
        lambda_client.update_function_configuration(
            FunctionName=func_name,
            Handler=f"{func_name.replace('-', '_')}_function.lambda_handler"
        )
        
        print(f"Updated {func_name}")

if __name__ == "__main__":
    update_all_bedrock_format()