import boto3
import zipfile
import json

def deploy_enhanced_lambdas():
    """Deploy enhanced Lambda functions"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    iam = boto3.client('iam')
    
    # Lambda execution role
    role_name = 'EnhancedLambdaExecutionRole'
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    try:
        role_response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        role_arn = role_response['Role']['Arn']
        
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        print("Created Lambda execution role")
        
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
        print("Using existing Lambda execution role")
    
    # Enhanced Lambda functions
    functions = [
        {
            'name': 'enhanced-market-demand',
            'file': 'lambda/enhanced-market-demand.py',
            'description': 'Enhanced market demand analysis with real APIs'
        },
        {
            'name': 'enhanced-competitor-scan',
            'file': 'lambda/enhanced-competitor-scan.py', 
            'description': 'Enhanced competitor analysis with Amazon/eBay APIs'
        },
        {
            'name': 'enhanced-capability-match',
            'file': 'lambda/enhanced-capability-match.py',
            'description': 'Enhanced capability analysis with Q Business integration'
        }
    ]
    
    deployed_functions = {}
    
    for func in functions:
        try:
            # Create zip file
            zip_filename = f"{func['name']}.zip"
            
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                zip_file.write(func['file'], 'lambda_function.py')
            
            # Create or update function
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
                    print(f"Created function: {func['name']}")
                    
                except lambda_client.exceptions.ResourceConflictException:
                    zip_file.seek(0)
                    response = lambda_client.update_function_code(
                        FunctionName=func['name'],
                        ZipFile=zip_file.read()
                    )
                    print(f"Updated function: {func['name']}")
            
            deployed_functions[func['name']] = response['FunctionArn']
            
        except Exception as e:
            print(f"Error with {func['name']}: {e}")
    
    return deployed_functions

if __name__ == "__main__":
    deploy_enhanced_lambdas()