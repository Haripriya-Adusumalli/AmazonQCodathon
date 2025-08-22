import boto3

def fix_enhanced_agent_permissions():
    """Add permissions for the enhanced agent"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    sts = boto3.client('sts')
    
    account_id = sts.get_caller_identity()['Account']
    enhanced_agent_id = 'BKWEM7GZQX'  # From your React config
    
    lambda_functions = ['enhanced-market-demand-copy', 'market-demand-agent']
    
    for func_name in lambda_functions:
        try:
            # Check if function exists
            try:
                lambda_client.get_function(FunctionName=func_name)
            except lambda_client.exceptions.ResourceNotFoundException:
                print(f"Function {func_name} does not exist")
                continue
            
            # Remove existing permission if any
            try:
                lambda_client.remove_permission(
                    FunctionName=func_name,
                    StatementId='bedrock-invoke'
                )
            except:
                pass
            
            # Add permission for enhanced agent
            lambda_client.add_permission(
                FunctionName=func_name,
                StatementId='bedrock-invoke',
                Action='lambda:InvokeFunction',
                Principal='bedrock.amazonaws.com',
                SourceArn=f'arn:aws:bedrock:us-east-1:{account_id}:agent/{enhanced_agent_id}'
            )
            
            print(f"Added permission for enhanced agent to {func_name}")
            
        except Exception as e:
            print(f"Error with {func_name}: {e}")

if __name__ == "__main__":
    fix_enhanced_agent_permissions()