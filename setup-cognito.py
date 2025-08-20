import boto3
import json
from botocore.exceptions import NoCredentialsError, ClientError

def create_cognito_user_pool():
    try:
        # Verify AWS credentials
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"Connected to AWS as: {identity['Arn']}")
        
        cognito = boto3.client('cognito-idp')
        
        # Create User Pool
        user_pool_response = cognito.create_user_pool(
            PoolName='ReactAppUserPool',
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': False,
                    'RequireLowercase': False,
                    'RequireNumbers': False,
                    'RequireSymbols': False
                }
            },
            UsernameAttributes=['email'],
            AutoVerifiedAttributes=['email'],
            VerificationMessageTemplate={
                'DefaultEmailOption': 'CONFIRM_WITH_CODE'
            }
        )
        
        user_pool_id = user_pool_response['UserPool']['Id']
        print(f"User Pool created: {user_pool_id}")
        
        # Create User Pool Client
        client_response = cognito.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName='ReactAppClient',
            GenerateSecret=False,
            ExplicitAuthFlows=['ADMIN_NO_SRP_AUTH', 'USER_PASSWORD_AUTH']
        )
        
        client_id = client_response['UserPoolClient']['ClientId']
        print(f"User Pool Client created: {client_id}")
        
        # Update aws-config.js
        config_content = f"""export const awsConfig = {{
  Auth: {{
    Cognito: {{
      userPoolId: '{user_pool_id}',
      userPoolClientId: '{client_id}',
      region: '{boto3.Session().region_name or "us-east-1"}'
    }}
  }}
}};"""
        
        with open('src/aws-config.js', 'w') as f:
            f.write(config_content)
        
        print("\nCognito setup complete!")
        print(f"User Pool ID: {user_pool_id}")
        print(f"Client ID: {client_id}")
        print("aws-config.js has been updated automatically.")
        
    except NoCredentialsError:
        print("ERROR: AWS credentials not configured. Run 'aws configure' first.")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    create_cognito_user_pool()