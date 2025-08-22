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

### Quick Setup
- **Windows**: Run `setup/setup.bat`
- **Linux/macOS**: Run `setup/setup.sh`
- **Manual**: Follow `setup/SETUP.md`

### Verification
```bash
python setup/verify-setup.py
```

For detailed instructions, see the [setup folder](setup/).

## Project Structure
```
├── setup/                          # Setup and installation files
│   ├── SETUP.md                    # Detailed setup guide
│   ├── QUICKSTART.md               # 5-minute setup guide
│   ├── setup.bat                   # Windows setup script
│   ├── setup.sh                    # Linux/macOS setup script
│   └── verify-setup.py             # Setup verification
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