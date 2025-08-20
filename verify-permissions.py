import boto3
import json

def verify_and_fix_permissions():
    try:
        iam = boto3.client('iam')
        role_name = 'Cognito_WeatherAppAuth_Role'
        
        print("Checking current IAM role permissions...")
        
        # Get current role policies
        try:
            policies = iam.list_role_policies(RoleName=role_name)
            print(f"Inline policies: {policies['PolicyNames']}")
            
            if 'BedrockAccess' in policies['PolicyNames']:
                policy = iam.get_role_policy(RoleName=role_name, PolicyName='BedrockAccess')
                print("Current policy document:")
                print(json.dumps(policy['PolicyDocument'], indent=2))
        except Exception as e:
            print(f"Error getting policies: {e}")
        
        # Create comprehensive Bedrock policy
        comprehensive_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "bedrock:InvokeAgent",
                        "bedrock:InvokeModel",
                        "bedrock:InvokeModelWithResponseStream",
                        "bedrock:ListFoundationModels",
                        "bedrock:GetFoundationModel"
                    ],
                    "Resource": "*"
                }
            ]
        }
        
        print("\nUpdating with comprehensive Bedrock permissions...")
        
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName='BedrockAccess',
            PolicyDocument=json.dumps(comprehensive_policy)
        )
        
        print("Policy updated successfully!")
        print("Permissions now include:")
        for action in comprehensive_policy["Statement"][0]["Action"]:
            print(f"  - {action}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_and_fix_permissions()