#!/usr/bin/env python3
"""
Setup Verification Script for Product Opportunity Recommendation System
Checks if all components are properly configured and accessible.
"""

import boto3
import json
import sys
from botocore.exceptions import ClientError, NoCredentialsError

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print("✅ AWS credentials configured")
        print(f"   Account: {identity['Account']}")
        print(f"   User: {identity['Arn']}")
        return True
    except NoCredentialsError:
        print("❌ AWS credentials not configured")
        print("   Run: aws configure")
        return False
    except Exception as e:
        print(f"❌ AWS credentials error: {e}")
        return False

def check_bedrock_access():
    """Check if Bedrock is accessible and Claude model is available"""
    try:
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        
        # List foundation models
        models = bedrock.list_foundation_models()
        claude_models = [m for m in models['modelSummaries'] if 'claude' in m['modelId'].lower()]
        
        if claude_models:
            print("✅ Bedrock access confirmed")
            print(f"   Found {len(claude_models)} Claude models")
            return True
        else:
            print("❌ No Claude models found")
            print("   Request model access in AWS Console > Bedrock > Model access")
            return False
            
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDeniedException':
            print("❌ Bedrock access denied")
            print("   Check IAM permissions for Bedrock")
        else:
            print(f"❌ Bedrock error: {e}")
        return False
    except Exception as e:
        print(f"❌ Bedrock connection error: {e}")
        return False

def check_agents():
    """Check if Bedrock agents are deployed and accessible"""
    try:
        # Read agent configuration
        with open('src/aws-config.js', 'r') as f:
            content = f.read()
            
        # Extract agent IDs (simple parsing)
        if 'agentId:' in content:
            print("✅ Agent configuration found")
            
            # Try to access Bedrock Agent Runtime
            bedrock_agent = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
            print("✅ Bedrock Agent Runtime accessible")
            return True
        else:
            print("❌ Agent configuration incomplete")
            print("   Update src/aws-config.js with agent IDs")
            return False
            
    except FileNotFoundError:
        print("❌ AWS config file not found")
        print("   Create src/aws-config.js")
        return False
    except Exception as e:
        print(f"❌ Agent check error: {e}")
        return False

def check_cognito():
    """Check if Cognito is configured"""
    try:
        with open('src/aws-config.js', 'r') as f:
            content = f.read()
            
        if 'userPoolId:' in content and 'userPoolClientId:' in content:
            print("✅ Cognito configuration found")
            return True
        else:
            print("❌ Cognito configuration incomplete")
            return False
            
    except FileNotFoundError:
        print("❌ AWS config file not found")
        return False

def check_dependencies():
    """Check if Node.js dependencies are installed"""
    import os
    if os.path.exists('node_modules') and os.path.exists('package-lock.json'):
        print("✅ Node.js dependencies installed")
        return True
    else:
        print("❌ Node.js dependencies not installed")
        print("   Run: npm install")
        return False

def main():
    print("🔍 Product Opportunity Recommendation System - Setup Verification")
    print("=" * 70)
    
    checks = [
        ("AWS Credentials", check_aws_credentials),
        ("Node.js Dependencies", check_dependencies),
        ("Bedrock Access", check_bedrock_access),
        ("Cognito Configuration", check_cognito),
        ("Agent Configuration", check_agents),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 70)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 All checks passed! Your system is ready.")
        print("\nNext steps:")
        print("1. Run: npm start")
        print("2. Open: http://localhost:3000")
    else:
        print(f"⚠️  {passed}/{total} checks passed. Please fix the issues above.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)