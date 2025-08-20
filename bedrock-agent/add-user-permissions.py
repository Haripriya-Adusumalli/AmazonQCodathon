import boto3
import json

def add_user_bedrock_permissions():
    try:
        iam = boto3.client('iam')
        sts = boto3.client('sts')
        
        # Get current user
        identity = sts.get_caller_identity()
        user_arn = identity['Arn']
        username = user_arn.split('/')[-1]
        
        print(f"Adding Bedrock permissions for user: {username}")
        
        # Create policy for Bedrock access
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "bedrock:InvokeModel",
                        "bedrock:InvokeModelWithResponseStream",
                        "bedrock-agent-runtime:InvokeAgent",
                        "bedrock:ListFoundationModels",
                        "bedrock:GetFoundationModel"
                    ],
                    "Resource": "*"
                }
            ]
        }
        
        # Create or update the policy
        policy_name = 'BedrockUserAccess'
        
        try:
            # Try to create the policy
            policy_response = iam.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_document),
                Description='Policy for Bedrock access'
            )
            policy_arn = policy_response['Policy']['Arn']
            print(f"Created policy: {policy_arn}")
        except iam.exceptions.EntityAlreadyExistsException:
            # Policy exists, get its ARN
            account_id = identity['Account']
            policy_arn = f"arn:aws:iam::{account_id}:policy/{policy_name}"
            print(f"Using existing policy: {policy_arn}")
        
        # Attach policy to user
        try:
            iam.attach_user_policy(
                UserName=username,
                PolicyArn=policy_arn
            )
            print(f"Attached policy to user: {username}")
        except Exception as e:
            if "already attached" in str(e).lower():
                print("Policy already attached to user")
            else:
                raise e
        
        print("User permissions updated successfully!")
        print("You can now test the Bedrock agent.")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nAlternative: You can manually add these permissions in the AWS Console:")
        print("1. Go to IAM > Users > your-username")
        print("2. Click 'Add permissions' > 'Attach policies directly'")
        print("3. Search for and attach: 'AmazonBedrockFullAccess'")

if __name__ == "__main__":
    add_user_bedrock_permissions()