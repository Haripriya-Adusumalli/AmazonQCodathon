import boto3
import json

def fix_iam_policy():
    try:
        iam = boto3.client('iam')
        role_name = 'Cognito_WeatherAppAuth_Role'
        
        # Correct Bedrock policy with proper permissions
        bedrock_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "bedrock:InvokeAgent",
                        "bedrock:InvokeModel",
                        "bedrock:InvokeModelWithResponseStream"
                    ],
                    "Resource": "*"
                }
            ]
        }
        
        print(f"Updating IAM policy for role: {role_name}")
        
        # Update the inline policy
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName='BedrockAccess',
            PolicyDocument=json.dumps(bedrock_policy)
        )
        
        print("✅ IAM policy updated successfully!")
        print("The role now has bedrock:InvokeAgent permission.")
        print("Try the React app again - it should work now.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_iam_policy()