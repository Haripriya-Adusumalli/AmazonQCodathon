# Product Opportunity Recommendation System - Setup Guide

A comprehensive AI-powered React application that identifies high-potential product opportunities using DCC (Demand + Competition + Capability) analysis, plus weather assistance.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- AWS CLI configured
- AWS account with appropriate permissions

### 1. Clone & Install
```bash
git clone <repository-url>
cd AQCodathon
npm install
```

### 2. Configure AWS Credentials
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region (us-east-1)
```

### 3. Enable Bedrock Model Access
1. Go to [AWS Console > Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
2. Click "Model access" in left sidebar
3. Click "Request model access"
4. Select "Anthropic Claude 3 Haiku" and submit request
5. Wait for approval (usually instant)

### 4. Deploy Backend Services

#### Deploy Weather Agent
```bash
cd bedrock-agent
python complete-deploy.py
```

#### Deploy Product Opportunity Agent
```bash
cd product-opportunity-agent
python simple-deploy.py
```

### 5. Update Configuration
After deployment, update `src/aws-config.js` with your agent IDs from the deployment outputs.

### 6. Run Application
```bash
npm start
```

The application will open at `http://localhost:3000`

## 📋 Detailed Setup Instructions

### AWS Permissions Required
Your AWS user/role needs these permissions:
- `AmazonBedrockFullAccess`
- `AWSLambdaFullAccess`
- `IAMFullAccess`
- `AmazonCognitoPowerUser`

### Manual Configuration Steps

#### 1. Cognito Setup (if not using existing)
```bash
python setup-cognito.py
```

#### 2. Verify Bedrock Access
```bash
python test-bedrock-direct.py
```

#### 3. Test Agent Deployment
```bash
cd bedrock-agent
python test-agent-simple.py
```

### Configuration Files

#### AWS Config (`src/aws-config.js`)
```javascript
export const awsConfig = {
  Auth: {
    Cognito: {
      userPoolId: 'YOUR_USER_POOL_ID',
      userPoolClientId: 'YOUR_CLIENT_ID',
      region: 'us-east-1',
      identityPoolId: 'YOUR_IDENTITY_POOL_ID'
    }
  }
};

export const bedrockConfig = {
  agentId: 'YOUR_WEATHER_AGENT_ID',
  aliasId: 'YOUR_WEATHER_ALIAS_ID',
  region: 'us-east-1'
};

export const productOpportunityConfig = {
  agentId: 'YOUR_PRODUCT_AGENT_ID',
  aliasId: 'YOUR_PRODUCT_ALIAS_ID',
  region: 'us-east-1'
};
```

## 🏗️ Architecture Overview

```
User → React App (Amplify) → Cognito Auth → Bedrock Agents → Lambda Functions → Claude 3 Haiku
```

### Components
- **Frontend**: React 18 with AWS Amplify UI
- **Authentication**: Amazon Cognito
- **AI Processing**: Amazon Bedrock with Claude 3 Haiku
- **Business Logic**: AWS Lambda functions
- **Agents**: Weather Assistant + Product Opportunity Analyzer

## 🎯 Usage

### Product Opportunity Analysis
1. Sign up/Sign in with Cognito
2. Navigate to "Product Opportunities" tab
3. Ask questions like:
   - "Analyze smart water bottle opportunity in India"
   - "What's the potential for eco-friendly phone cases?"
   - "Should we launch a fitness tracking app?"

### Weather Assistant
1. Navigate to "Weather Assistant" tab
2. Ask weather-related questions:
   - "What's the weather like today?"
   - "Tell me about different types of clouds"

## 🧪 Testing

```bash
# Run all tests
npm test

# Run specific test suites
npm run test:chatbots
npm run test:backend
npm run test:lambda

# Run with coverage
npm run test:coverage
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Bedrock Access Denied
```bash
# Check model access
python simple-bedrock-check.py

# Fix permissions
python fix-bedrock-permissions.py
```

#### 2. Lambda Function Errors
```bash
# Check Lambda logs
python check-lambda-logs.py

# Update Lambda permissions
python fix-lambda-permissions.py
```

#### 3. Agent Not Responding
```bash
# Test agent directly
python test-agent-simple.py

# Check agent configuration
python check-agent-config.py
```

### Environment Variables
Create `.env` file in root:
```
REACT_APP_AWS_REGION=us-east-1
REACT_APP_USER_POOL_ID=your_pool_id
REACT_APP_CLIENT_ID=your_client_id
```

## 📁 Project Structure
```
├── src/
│   ├── App.js                      # Main application
│   ├── ProductDashboard.js         # Tabbed dashboard
│   ├── ProductOpportunityChat.js   # Product analysis chat
│   ├── BedrockChat.js              # Weather chat component
│   └── aws-config.js               # AWS configuration
├── bedrock-agent/
│   ├── complete-deploy.py          # Weather agent deployment
│   ├── product-opportunity-agent/  # Product opportunity system
│   └── lambda/                     # Lambda functions
└── public/                         # Static assets
```

## 🚀 Deployment

### Production Build
```bash
npm run build
```

### Deploy to AWS Amplify
1. Connect your repository to AWS Amplify
2. Configure build settings:
   ```yaml
   version: 1
   frontend:
     phases:
       preBuild:
         commands:
           - npm install
       build:
         commands:
           - npm run build
     artifacts:
       baseDirectory: build
       files:
         - '**/*'
   ```

## 📚 Additional Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [React Documentation](https://react.dev/)
- [AWS Amplify Documentation](https://docs.amplify.aws/)

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review AWS CloudWatch logs
3. Test individual components using provided scripts