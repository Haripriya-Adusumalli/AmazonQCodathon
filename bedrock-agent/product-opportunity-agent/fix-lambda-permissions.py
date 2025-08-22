import boto3

def fix_lambda_permissions():
    """Fix Lambda permissions for Bedrock agent"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    sts = boto3.client('sts')
    
    # Get account ID
    account_id = sts.get_caller_identity()['Account']
    agent_id = 'DKPL7RP9OU'
    
    lambda_functions = ['market-demand-agent', 'competitor-scan-agent', 'capability-match-agent']
    
    for func_name in lambda_functions:
        try:
            # Remove existing permission if any
            try:
                lambda_client.remove_permission(
                    FunctionName=func_name,
                    StatementId='bedrock-invoke'
                )
            except:
                pass
            
            # Add correct permission
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
    fix_lambda_permissions()