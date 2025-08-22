import boto3
import zipfile

def fix_competitor_scan():
    """Fix competitor scan function to work without external dependencies"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Update to original working version
    competitor_zip = "competitor-scan-fixed.zip"
    with zipfile.ZipFile(competitor_zip, 'w') as zip_file:
        zip_file.write("lambda/competitor-scan-function.py", "competitor-scan-function.py")
    
    with open(competitor_zip, 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='competitor-scan-agent',
            ZipFile=zip_file.read()
        )
    
    print("Fixed competitor-scan-agent")

if __name__ == "__main__":
    fix_competitor_scan()