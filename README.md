# React App with Amazon Cognito Authentication & Bedrock Agent

A React application featuring Amazon Cognito authentication and a Bedrock AI agent for weather assistance.

## Features
- 🔐 Amazon Cognito authentication (sign up, sign in, forgot password)
- 🤖 Amazon Bedrock AI agent integration
- 💬 Real-time chat interface with weather assistant
- 🎨 Modern UI with gradient background
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

### 4. Deploy Bedrock Agent
```bash
cd bedrock-agent
python complete-deploy.py
```

### 5. Configure Application
Update `src/aws-config.js` with your values (already configured for demo).

### 6. Run the Application
```bash
npm start
```

## Project Structure
```
├── src/
│   ├── App.js              # Main application
│   ├── Dashboard.js        # User dashboard
│   ├── BedrockChat.js      # AI chat component
│   ├── BedrockChat.css     # Chat styling
│   └── aws-config.js       # AWS configuration
├── bedrock-agent/
│   ├── deploy.py           # Agent deployment
│   ├── agent-schema.json   # API schema
│   └── lambda/             # Lambda functions
└── README.md
```

## Usage
1. Sign up/Sign in with Cognito
2. Chat with the weather assistant
3. Ask questions like:
   - "What's the weather like today?"
   - "Tell me about different types of clouds"
   - "How do hurricanes form?"

## Technologies
- React 18
- AWS Amplify
- Amazon Cognito
- Amazon Bedrock
- AWS SDK v3