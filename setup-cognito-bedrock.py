import boto3
import json

def setup_cognito_bedrock_permissions():
    try:
        iam = boto3.client('iam')
        cognito_identity = boto3.client('cognito-identity')
        
        # Create IAM role for authenticated Cognito users
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
                            "cognito-identity.amazonaws.com:aud": "YOUR_IDENTITY_POOL_ID"
                        },
                        "ForAnyValue:StringLike": {
                            "cognito-identity.amazonaws.com:amr": "authenticated"
                        }
                    }
                }
            ]
        }
        
        # Bedrock permissions policy
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
        
        role_name = "CognitoBedrockRole"
        
        # Create role
        try:
            role_response = iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description="Role for Cognito users to access Bedrock"
            )
            print(f"Created role: {role_response['Role']['Arn']}")
        except iam.exceptions.EntityAlreadyExistsException:
            print(f"Role {role_name} already exists")
        
        # Create and attach policy
        policy_name = "CognitoBedrockPolicy"
        try:
            policy_response = iam.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(bedrock_policy),
                Description="Bedrock access for Cognito users"
            )
            policy_arn = policy_response['Policy']['Arn']
        except iam.exceptions.EntityAlreadyExistsException:
            sts = boto3.client('sts')
            account_id = sts.get_caller_identity()['Account']
            policy_arn = f"arn:aws:iam::{account_id}:policy/{policy_name}"
        
        # Attach policy to role
        try:
            iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            print("Policy attached to role")
        except Exception as e:
            if "already attached" not in str(e).lower():
                print(f"Error attaching policy: {e}")
        
        print("\nNext steps:")
        print("1. Create a Cognito Identity Pool in AWS Console")
        print("2. Link it to your User Pool")
        print(f"3. Set the authenticated role to: {role_name}")
        print("4. Update aws-config.js with the Identity Pool ID")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_cognito_bedrock_permissions()