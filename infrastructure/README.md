# Infrastructure as Code

This directory contains CloudFormation and Terraform scripts to deploy the complete Product Opportunity Recommendation System infrastructure.

## 🏗️ Architecture Components

- **Amazon Cognito**: User authentication (User Pool, Identity Pool)
- **AWS Lambda**: Serverless functions for business logic
- **Amazon Bedrock**: AI agents for weather and product analysis
- **IAM Roles**: Secure access permissions

## 📁 Directory Structure

```
infrastructure/
├── cloudformation/
│   ├── main-stack.yaml          # Core infrastructure
│   ├── bedrock-agents.yaml      # Bedrock agents configuration
│   └── parameters.json          # Stack parameters
├── terraform/
│   ├── main.tf                  # Core infrastructure
│   ├── outputs.tf               # Output values
│   ├── bedrock-agents.tf        # Bedrock agents (placeholder)
│   └── terraform.tfvars.example # Example variables
├── deploy.sh                    # Linux/macOS deployment script
├── deploy.bat                   # Windows deployment script
└── README.md                    # This file
```

## 🚀 Quick Deployment

### Option 1: CloudFormation (Recommended)

**Linux/macOS:**
```bash
cd infrastructure
chmod +x deploy.sh
./deploy.sh cloudformation
```

**Windows:**
```cmd
cd infrastructure
deploy.bat cloudformation
```

### Option 2: Terraform

**Linux/macOS:**
```bash
cd infrastructure
./deploy.sh terraform
```

**Windows:**
```cmd
cd infrastructure
deploy.bat terraform
```

## ⚙️ Manual Setup

### CloudFormation

1. **Configure parameters:**
   ```bash
   cp cloudformation/parameters.json cloudformation/parameters-prod.json
   # Edit parameters-prod.json with your values
   ```

2. **Deploy main stack:**
   ```bash
   aws cloudformation deploy \
     --template-file cloudformation/main-stack.yaml \
     --stack-name product-opportunity-system-main \
     --parameter-overrides file://cloudformation/parameters-prod.json \
     --capabilities CAPABILITY_IAM \
     --region us-east-1
   ```

3. **Deploy Bedrock agents:**
   ```bash
   # Get ARNs from main stack outputs first
   aws cloudformation deploy \
     --template-file cloudformation/bedrock-agents.yaml \
     --stack-name product-opportunity-system-agents \
     --parameter-overrides \
       ProjectName=product-opportunity-system \
       Environment=prod \
       BedrockAgentRoleArn=<ROLE_ARN> \
       WeatherFunctionArn=<FUNCTION_ARN> \
       # ... other parameters
   ```

### Terraform

1. **Configure variables:**
   ```bash
   cd terraform
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

2. **Deploy infrastructure:**
   ```bash
   terraform init
   terraform plan -var-file="terraform.tfvars"
   terraform apply -var-file="terraform.tfvars"
   ```

3. **Deploy Bedrock agents separately:**
   ```bash
   # Use CloudFormation template or Python deployment scripts
   cd ../bedrock-agent
   python simple-deploy.py
   ```

## 🔧 Configuration

### Required Parameters

- `ProjectName`: Name prefix for all resources
- `Environment`: Environment name (dev, staging, prod)
- `WeatherApiKey`: OpenWeatherMap API key

### Optional Customizations

- **Region**: Change AWS region in parameters/variables
- **Lambda Runtime**: Update runtime versions in templates
- **Cognito Policies**: Modify password policies and user attributes
- **IAM Permissions**: Adjust permissions for security requirements

## 📊 Outputs

After deployment, the following values are available:

### CloudFormation Outputs
- User Pool ID
- User Pool Client ID
- Identity Pool ID
- Lambda Function ARNs
- Bedrock Agent IDs and Alias IDs

### Terraform Outputs
- All CloudFormation outputs plus
- Generated `aws-config.js` content

## 🔍 Verification

1. **Check stack status:**
   ```bash
   aws cloudformation describe-stacks \
     --stack-name product-opportunity-system-main
   ```

2. **Test Lambda functions:**
   ```bash
   aws lambda invoke \
     --function-name product-opportunity-system-dev-weather \
     --payload '{"inputText":"London"}' \
     response.json
   ```

3. **Verify Bedrock agents:**
   ```bash
   aws bedrock-agent list-agents
   ```

## 🧹 Cleanup

### CloudFormation
```bash
aws cloudformation delete-stack --stack-name product-opportunity-system-agents
aws cloudformation delete-stack --stack-name product-opportunity-system-main
```

### Terraform
```bash
cd terraform
terraform destroy -var-file="terraform.tfvars"
```

## 🚨 Troubleshooting

### Common Issues

1. **Bedrock Model Access**: Ensure Claude models are enabled in AWS Console
2. **IAM Permissions**: Check that deployment user has sufficient permissions
3. **Region Availability**: Verify Bedrock is available in your chosen region
4. **API Keys**: Ensure external API keys are valid and have sufficient quotas

### Debug Commands

```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify Bedrock access
aws bedrock list-foundation-models --region us-east-1

# Check CloudFormation events
aws cloudformation describe-stack-events \
  --stack-name product-opportunity-system-main
```

## 📚 Additional Resources

- [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [Amazon Cognito Developer Guide](https://docs.aws.amazon.com/cognito/)