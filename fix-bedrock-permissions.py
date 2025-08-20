import boto3
import json

def create_identity_pool_and_role():
    try:
        cognito_identity = boto3.client('cognito-identity', region_name='us-east-1')
        iam = boto3.client('iam')
        sts = boto3.client('sts')
        
        account_id = sts.get_caller_identity()['Account']
        user_pool_id = 'us-east-1_liYtIs82R'
        client_id = '5gjbh0bueph4233e711bmukh6c'
        
        print("Creating Cognito Identity Pool...")
        
        try:
            identity_pool = cognito_identity.create_identity_pool(
                IdentityPoolName='WeatherAppIdentityPool',
                AllowUnauthenticatedIdentities=False,
                CognitoIdentityProviders=[
                    {
                        'ProviderName': f'cognito-idp.us-east-1.amazonaws.com/{user_pool_id}',
                        'ClientId': client_id,
                        'ServerSideTokenCheck': False
                    }
                ]
            )
            identity_pool_id = identity_pool['IdentityPoolId']
            print(f"Created Identity Pool: {identity_pool_id}")
        except Exception as e:
            if "already exists" in str(e).lower():
                pools = cognito_identity.list_identity_pools(MaxResults=60)
                identity_pool_id = None
                for pool in pools['IdentityPools']:
                    if 'WeatherApp' in pool['IdentityPoolName']:
                        identity_pool_id = pool['IdentityPoolId']
                        break
                if not identity_pool_id:
                    raise e
                print(f"Using existing Identity Pool: {identity_pool_id}")
            else:
                raise e
        
        role_name = 'Cognito_WeatherAppAuth_Role'
        
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Federated": "cognito-identity.amazonaws.com"
                    },
                    "Action": "sts:AssumeRoleWithWebIdentity",
                    "Condition": {
                        "StringEquals": {
                            "cognito-identity.amazonaws.com:aud": identity_pool_id
                        },
                        "ForAnyValue:StringLike": {
                            "cognito-identity.amazonaws.com:amr": "authenticated"
                        }
                    }
                }
            ]
        }
        
        try:
            role_response = iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description="Role for authenticated Cognito users to access Bedrock"
            )
            role_arn = role_response['Role']['Arn']
            print(f"Created role: {role_arn}")
        except iam.exceptions.EntityAlreadyExistsException:
            role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
            print(f"Using existing role: {role_arn}")
        
        bedrock_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "bedrock:InvokeModel",
                        "bedrock:InvokeModelWithResponseStream",
                        "bedrock-agent-runtime:InvokeAgent"
                    ],
                    "Resource": "*"
                }
            ]
        }
        
        try:
            iam.put_role_policy(
                RoleName=role_name,
                PolicyName='BedrockAccess',
                PolicyDocument=json.dumps(bedrock_policy)
            )
            print("Attached Bedrock policy to role")
        except Exception as e:
            print(f"Policy attachment: {e}")
        
        try:
            cognito_identity.set_identity_pool_roles(
                IdentityPoolId=identity_pool_id,
                Roles={
                    'authenticated': role_arn
                }
            )
            print("Set Identity Pool roles")
        except Exception as e:
            print(f"Setting roles: {e}")
        
        config_content = f"""export const awsConfig = {{
  Auth: {{
    Cognito: {{
      userPoolId: '{user_pool_id}',
      userPoolClientId: '{client_id}',
      region: 'us-east-1',
      identityPoolId: '{identity_pool_id}'
    }}
  }}
}};

export const bedrockConfig = {{
  agentId: 'E7QJOXGNCA',
  aliasId: 'JJYE1KNRVY',
  region: 'us-east-1'
}};"""
        
        with open('src/aws-config.js', 'w') as f:
            f.write(config_content)
        
        print("Setup complete!")
        print(f"Identity Pool ID: {identity_pool_id}")
        print("Updated aws-config.js with Identity Pool ID")
        print("You can now test the React application with Bedrock access.")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_identity_pool_and_role()