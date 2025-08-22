import boto3

def fix_permissions_only():
    """Only fix IAM permissions for existing Lambda function"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    func_name = 'market-demand-agent'
    
    try:
        # Remove existing bedrock permission if any
        try:
            lambda_client.remove_permission(
                FunctionName=func_name,
                StatementId='bedrock-invoke'
            )
        except:
            pass
        
        # Add permission for Bedrock to invoke Lambda
        lambda_client.add_permission(
            FunctionName=func_name,
            StatementId='bedrock-invoke',
            Action='lambda:InvokeFunction',
            Principal='bedrock.amazonaws.com'
        )
        print(f"Fixed permissions for {func_name}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_permissions_only()