import boto3
import zipfile
import os

def update_existing_lambdas():
    """Update existing Lambda functions with enhanced code"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Copy enhanced code to existing function files
    enhanced_files = [
        ('lambda/enhanced-market-demand.py', 'lambda/market-demand-function.py'),
        ('lambda/enhanced-competitor-scan.py', 'lambda/competitor-scan-function.py'),
        ('lambda/enhanced-capability-match.py', 'lambda/capability-match-function.py')
    ]
    
    for enhanced_file, original_file in enhanced_files:
        try:
            with open(enhanced_file, 'r') as ef:
                enhanced_code = ef.read()
            
            with open(original_file, 'w') as of:
                of.write(enhanced_code)
            
            print(f"Updated {original_file} with enhanced code")
            
        except Exception as e:
            print(f"Error updating {original_file}: {e}")
    
    # Update Lambda functions
    functions = [
        ('market-demand-agent', 'lambda/market-demand-function.py'),
        ('competitor-scan-agent', 'lambda/competitor-scan-function.py'),
        ('capability-match-agent', 'lambda/capability-match-function.py')
    ]
    
    for func_name, py_file in functions:
        try:
            # Create zip file
            zip_filename = f"{func_name}-enhanced.zip"
            
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                zip_file.write(py_file, 'lambda_function.py')
            
            # Update function code
            with open(zip_filename, 'rb') as zip_file:
                lambda_client.update_function_code(
                    FunctionName=func_name,
                    ZipFile=zip_file.read()
                )
            
            print(f"Updated Lambda function: {func_name}")
            
            # Clean up
            os.remove(zip_filename)
            
        except Exception as e:
            print(f"Error updating {func_name}: {e}")

if __name__ == "__main__":
    update_existing_lambdas()