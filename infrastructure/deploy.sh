#!/bin/bash

# Product Opportunity Recommendation System - Deployment Script

set -e

PROJECT_NAME="product-opportunity-system"
ENVIRONMENT="dev"
REGION="us-east-1"

echo "🚀 Deploying Product Opportunity Recommendation System"
echo "=================================================="

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI not configured. Run 'aws configure' first."
    exit 1
fi

echo "✅ AWS CLI configured"

# Deploy using CloudFormation
deploy_cloudformation() {
    echo "📦 Deploying with CloudFormation..."
    
    # Deploy main stack
    aws cloudformation deploy \
        --template-file cloudformation/main-stack.yaml \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-main" \
        --parameter-overrides file://cloudformation/parameters.json \
        --capabilities CAPABILITY_IAM \
        --region $REGION
    
    echo "✅ Main stack deployed"
    
    # Get outputs from main stack
    BEDROCK_ROLE_ARN=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-main" \
        --query 'Stacks[0].Outputs[?OutputKey==`BedrockAgentRoleArn`].OutputValue' \
        --output text \
        --region $REGION)
    
    WEATHER_FUNCTION_ARN=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-main" \
        --query 'Stacks[0].Outputs[?OutputKey==`WeatherFunctionArn`].OutputValue' \
        --output text \
        --region $REGION)
    
    MARKET_DEMAND_FUNCTION_ARN=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-main" \
        --query 'Stacks[0].Outputs[?OutputKey==`MarketDemandFunctionArn`].OutputValue' \
        --output text \
        --region $REGION)
    
    COMPETITOR_SCAN_FUNCTION_ARN=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-main" \
        --query 'Stacks[0].Outputs[?OutputKey==`CompetitorScanFunctionArn`].OutputValue' \
        --output text \
        --region $REGION)
    
    CAPABILITY_MATCH_FUNCTION_ARN=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-main" \
        --query 'Stacks[0].Outputs[?OutputKey==`CapabilityMatchFunctionArn`].OutputValue' \
        --output text \
        --region $REGION)
    
    # Deploy Bedrock agents stack
    aws cloudformation deploy \
        --template-file cloudformation/bedrock-agents.yaml \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-agents" \
        --parameter-overrides \
            ProjectName=$PROJECT_NAME \
            Environment=$ENVIRONMENT \
            BedrockAgentRoleArn=$BEDROCK_ROLE_ARN \
            WeatherFunctionArn=$WEATHER_FUNCTION_ARN \
            MarketDemandFunctionArn=$MARKET_DEMAND_FUNCTION_ARN \
            CompetitorScanFunctionArn=$COMPETITOR_SCAN_FUNCTION_ARN \
            CapabilityMatchFunctionArn=$CAPABILITY_MATCH_FUNCTION_ARN \
        --capabilities CAPABILITY_IAM \
        --region $REGION
    
    echo "✅ Bedrock agents deployed"
    
    # Get final outputs
    USER_POOL_ID=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-main" \
        --query 'Stacks[0].Outputs[?OutputKey==`UserPoolId`].OutputValue' \
        --output text \
        --region $REGION)
    
    USER_POOL_CLIENT_ID=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-main" \
        --query 'Stacks[0].Outputs[?OutputKey==`UserPoolClientId`].OutputValue' \
        --output text \
        --region $REGION)
    
    IDENTITY_POOL_ID=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-main" \
        --query 'Stacks[0].Outputs[?OutputKey==`IdentityPoolId`].OutputValue' \
        --output text \
        --region $REGION)
    
    WEATHER_AGENT_ID=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-agents" \
        --query 'Stacks[0].Outputs[?OutputKey==`WeatherAgentId`].OutputValue' \
        --output text \
        --region $REGION)
    
    WEATHER_AGENT_ALIAS_ID=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-agents" \
        --query 'Stacks[0].Outputs[?OutputKey==`WeatherAgentAliasId`].OutputValue' \
        --output text \
        --region $REGION)
    
    PRODUCT_AGENT_ID=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-agents" \
        --query 'Stacks[0].Outputs[?OutputKey==`ProductOpportunityAgentId`].OutputValue' \
        --output text \
        --region $REGION)
    
    PRODUCT_AGENT_ALIAS_ID=$(aws cloudformation describe-stacks \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}-agents" \
        --query 'Stacks[0].Outputs[?OutputKey==`ProductOpportunityAgentAliasId`].OutputValue' \
        --output text \
        --region $REGION)
    
    # Generate aws-config.js
    cat > ../src/aws-config.js << EOF
export const awsConfig = {
  Auth: {
    Cognito: {
      userPoolId: '${USER_POOL_ID}',
      userPoolClientId: '${USER_POOL_CLIENT_ID}',
      region: '${REGION}',
      identityPoolId: '${IDENTITY_POOL_ID}'
    }
  }
};

export const bedrockConfig = {
  agentId: '${WEATHER_AGENT_ID}',
  aliasId: '${WEATHER_AGENT_ALIAS_ID}',
  region: '${REGION}'
};

export const productOpportunityConfig = {
  agentId: '${PRODUCT_AGENT_ID}',
  aliasId: '${PRODUCT_AGENT_ALIAS_ID}',
  region: '${REGION}'
};
EOF
    
    echo "✅ AWS configuration updated"
}

# Deploy using Terraform
deploy_terraform() {
    echo "📦 Deploying with Terraform..."
    
    cd terraform
    
    # Initialize Terraform
    terraform init
    
    # Plan deployment
    terraform plan -var-file="terraform.tfvars"
    
    # Apply deployment
    terraform apply -var-file="terraform.tfvars" -auto-approve
    
    # Generate aws-config.js from outputs
    terraform output -json > outputs.json
    
    USER_POOL_ID=$(cat outputs.json | jq -r '.user_pool_id.value')
    USER_POOL_CLIENT_ID=$(cat outputs.json | jq -r '.user_pool_client_id.value')
    IDENTITY_POOL_ID=$(cat outputs.json | jq -r '.identity_pool_id.value')
    
    cat > ../../src/aws-config.js << EOF
export const awsConfig = {
  Auth: {
    Cognito: {
      userPoolId: '${USER_POOL_ID}',
      userPoolClientId: '${USER_POOL_CLIENT_ID}',
      region: '${REGION}',
      identityPoolId: '${IDENTITY_POOL_ID}'
    }
  }
};

// Note: Bedrock agents need to be deployed separately using CloudFormation or Python scripts
export const bedrockConfig = {
  agentId: 'DEPLOY_AGENTS_SEPARATELY',
  aliasId: 'DEPLOY_AGENTS_SEPARATELY',
  region: '${REGION}'
};

export const productOpportunityConfig = {
  agentId: 'DEPLOY_AGENTS_SEPARATELY',
  aliasId: 'DEPLOY_AGENTS_SEPARATELY',
  region: '${REGION}'
};
EOF
    
    cd ..
    echo "✅ Terraform deployment complete"
    echo "⚠️  Deploy Bedrock agents separately using CloudFormation or Python scripts"
}

# Main deployment logic
case "${1:-cloudformation}" in
    "cloudformation"|"cf")
        deploy_cloudformation
        ;;
    "terraform"|"tf")
        deploy_terraform
        ;;
    *)
        echo "Usage: $0 [cloudformation|terraform]"
        echo "Default: cloudformation"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo "=================================================="
echo "Next steps:"
echo "1. Update src/aws-config.js with your API keys if needed"
echo "2. Run: npm install && npm start"
echo "3. Open: http://localhost:3000"
echo ""