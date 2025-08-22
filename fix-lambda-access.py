import boto3
import json

def fix_lambda_access():
    """Fix Lambda function permissions for Bedrock agent access"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    sts = boto3.client('sts')
    
    # Get account ID
    account_id = sts.get_caller_identity()['Account']
    
    # Lambda function name that's failing
    func_name = 'market-demand-agent'
    
    try:
        # Get current policy
        try:
            policy = lambda_client.get_policy(FunctionName=func_name)
            print(f"Current policy for {func_name}:")
            print(json.dumps(json.loads(policy['Policy']), indent=2))
        except lambda_client.exceptions.ResourceNotFoundException:
            print(f"No policy found for {func_name}")
        
        # Remove any existing bedrock permissions
        try:
            lambda_client.remove_permission(
                FunctionName=func_name,
                StatementId='bedrock-invoke'
            )
            print("Removed existing bedrock permission")
        except:
            pass
        
        # Add correct permission for Bedrock
        lambda_client.add_permission(
            FunctionName=func_name,
            StatementId='bedrock-invoke',
            Action='lambda:InvokeFunction',
            Principal='bedrock.amazonaws.com'
        )
        print(f"Added Bedrock permission to {func_name}")
        
        # Verify the function exists and is accessible
        response = lambda_client.get_function(FunctionName=func_name)
        print(f"Function {func_name} exists and is accessible")
        print(f"Runtime: {response['Configuration']['Runtime']}")
        print(f"Handler: {response['Configuration']['Handler']}")
        
    except Exception as e:
        print(f"Error fixing {func_name}: {e}")
        
        # Try to get more details about the error
        try:
            response = lambda_client.get_function(FunctionName=func_name)
            print("Function exists but permission issue")
        except lambda_client.exceptions.ResourceNotFoundException:
            print("Function does not exist - need to redeploy")
        except Exception as inner_e:
            print(f"Additional error: {inner_e}")

if __name__ == "__main__":
    fix_lambda_access()