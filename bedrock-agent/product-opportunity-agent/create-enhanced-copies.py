import boto3
import zipfile
import json
import time

def create_enhanced_copies():
    """Create new enhanced Lambda function copies"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    iam = boto3.client('iam')
    
    # Wait for role propagation and get role ARN
    try:
        role_arn = iam.get_role(RoleName='EnhancedLambdaExecutionRole')['Role']['Arn']
    except:
        # Create role if it doesn't exist
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }]
        }
        
        role_response = iam.create_role(
            RoleName='EnhancedLambdaExecutionRole',
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        role_arn = role_response['Role']['Arn']
        
        iam.attach_role_policy(
            RoleName='EnhancedLambdaExecutionRole',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        print("Created new Lambda execution role")
        time.sleep(10)  # Wait for role propagation
    
    # Enhanced Lambda functions
    functions = [
        {
            'name': 'enhanced-market-demand-copy',
            'file': 'lambda/enhanced-market-demand.py',
            'description': 'Enhanced market demand with real APIs - copy'
        },
        {
            'name': 'enhanced-competitor-scan-copy',
            'file': 'lambda/enhanced-competitor-scan.py',
            'description': 'Enhanced competitor scan with real APIs - copy'
        },
        {
            'name': 'enhanced-capability-match-copy',
            'file': 'lambda/enhanced-capability-match.py',
            'description': 'Enhanced capability match with Q Business - copy'
        }
    ]
    
    created_functions = {}
    
    for func in functions:
        try:
            zip_filename = f"{func['name']}.zip"
            
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                zip_file.write(func['file'], 'lambda_function.py')
            
            with open(zip_filename, 'rb') as zip_file:
                try:
                    response = lambda_client.create_function(
                        FunctionName=func['name'],
                        Runtime='python3.9',
                        Role=role_arn,
                        Handler='lambda_function.lambda_handler',
                        Code={'ZipFile': zip_file.read()},
                        Description=func['description'],
                        Timeout=30,
                        MemorySize=256
                    )
                    print(f"Created: {func['name']}")
                    
                except lambda_client.exceptions.ResourceConflictException:
                    zip_file.seek(0)
                    response = lambda_client.update_function_code(
                        FunctionName=func['name'],
                        ZipFile=zip_file.read()
                    )
                    print(f"Updated: {func['name']}")
                    response = lambda_client.get_function(FunctionName=func['name'])
            
            created_functions[func['name']] = response['Configuration']['FunctionArn']
            
        except Exception as e:
            print(f"Error with {func['name']}: {e}")
    
    return created_functions

if __name__ == "__main__":
    create_enhanced_copies()