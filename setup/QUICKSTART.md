# 🚀 Quick Start Guide

Get the Product Opportunity Recommendation System running in 5 minutes!

## Prerequisites
- Node.js 18+
- Python 3.7+
- AWS CLI configured
- AWS account with Bedrock access

## Option 1: Automated Setup (Recommended)

### Windows
```cmd
setup.bat
```

### Linux/macOS
```bash
chmod +x setup.sh
./setup.sh
```

## Option 2: Manual Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure AWS
```bash
aws configure
# Enter your credentials and set region to us-east-1
```

### 3. Enable Bedrock Models
1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Click "Model access" → "Request model access"
3. Select "Anthropic Claude 3 Haiku" → Submit

### 4. Deploy Agents
```bash
# Weather agent
cd bedrock-agent
python complete-deploy.py

# Product opportunity agent  
cd product-opportunity-agent
python simple-deploy.py
cd ../..
```

### 5. Update Configuration
Edit `src/aws-config.js` with your agent IDs from deployment outputs.

### 6. Start Application
```bash
npm start
```

## Verification

Run the verification script to check your setup:
```bash
python verify-setup.py
```

## Troubleshooting

### Common Issues

**"Access Denied" errors:**
```bash
python fix-bedrock-permissions.py
```

**Agent not responding:**
```bash
python test-agent-simple.py
```

**Lambda errors:**
```bash
python check-lambda-logs.py
```

## Usage

1. **Sign Up/Sign In** with Cognito authentication
2. **Product Opportunities Tab**: Ask about market opportunities
   - "Analyze smart water bottle opportunity in India"
   - "What's the potential for eco-friendly phone cases?"
3. **Weather Assistant Tab**: Ask weather questions
   - "What's the weather like today?"
   - "How do hurricanes form?"

## Next Steps

- Review [SETUP.md](SETUP.md) for detailed instructions
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system overview
- Run tests with `npm test`

## Support

If you encounter issues:
1. Run `python verify-setup.py` to diagnose problems
2. Check AWS CloudWatch logs
3. Review the troubleshooting section in SETUP.md