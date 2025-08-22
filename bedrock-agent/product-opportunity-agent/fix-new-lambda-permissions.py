import boto3

def fix_new_lambda_permissions():
    """Add permissions for the new Lambda function"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    sts = boto3.client('sts')
    
    account_id = sts.get_caller_identity()['Account']
    agent_id = 'DKPL7RP9OU'  # Your agent ID
    
    func_name = 'enhanced-market-demand-copy'
    
    try:
        # Remove existing permission if any
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
            Principal='bedrock.amazonaws.com',
            SourceArn=f'arn:aws:bedrock:us-east-1:{account_id}:agent/{agent_id}'
        )
        
        print(f"Added permission to {func_name}")
        
    except Exception as e:
        print(f"Error with {func_name}: {e}")

if __name__ == "__main__":
    fix_new_lambda_permissions()