# Product Opportunity Recommendation System

A comprehensive AI-powered React application that identifies high-potential product opportunities using DCC (Demand + Competition + Capability) analysis, plus weather assistance.

## Features
- 🔐 Amazon Cognito authentication (sign up, sign in, forgot password)
- 🎯 Product Opportunity Analyzer with DCC scoring
- 📊 Real-time market demand, competition & capability analysis
- 🤖 Amazon Bedrock AI agent integration
- 💬 Dual chat interfaces (Product Opportunities + Weather)
- 🎨 Modern tabbed UI with interactive dashboards
- 📱 Responsive design

## Setup Instructions

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure AWS Credentials
```bash
aws configure
```

### 3. Enable Bedrock Model Access
1. Go to AWS Console > Amazon Bedrock
2. Click "Model access" in left sidebar
3. Click "Request model access"
4. Select "Anthropic Claude 3 Haiku" and submit

### 4. Deploy Bedrock Agents
```bash
# Deploy weather agent
cd bedrock-agent
python complete-deploy.py

# Deploy product opportunity agent
cd product-opportunity-agent
python simple-deploy.py
```

### 5. Configure Application
Update `src/aws-config.js` with your agent IDs from deployment outputs.

### 6. Run the Application
```bash
npm start
```

## Project Structure
```
├── src/
│   ├── App.js                      # Main application
│   ├── ProductDashboard.js         # Tabbed dashboard
│   ├── ProductOpportunityChat.js   # Product analysis chat
│   ├── ProductOpportunityChat.css  # Product chat styling
│   ├── BedrockChat.js              # Weather chat component
│   ├── BedrockChat.css             # Weather chat styling
│   └── aws-config.js               # AWS configuration
├── bedrock-agent/
│   ├── deploy.py                   # Weather agent deployment
│   ├── product-opportunity-agent/  # Product opportunity system
│   │   ├── simple-deploy.py        # Quick deployment
│   │   ├── lambda/                 # Domain agent functions
│   │   └── README.md               # System documentation
│   └── lambda/                     # Weather Lambda functions
└── README.md
```

## Usage

### Product Opportunity Analysis
1. Sign up/Sign in with Cognito
2. Navigate to "Product Opportunities" tab
3. Ask questions like:
   - "Analyze smart water bottle opportunity in India"
   - "What's the potential for eco-friendly phone cases?"
   - "Should we launch a fitness tracking app?"
4. Review DCC scores and recommendations

### Weather Assistant
1. Navigate to "Weather Assistant" tab
2. Ask weather-related questions:
   - "What's the weather like today?"
   - "Tell me about different types of clouds"
   - "How do hurricanes form?"

## Technologies
- React 18
- AWS Amplify
- Amazon Cognito
- Amazon Bedrock
- AWS SDK v3