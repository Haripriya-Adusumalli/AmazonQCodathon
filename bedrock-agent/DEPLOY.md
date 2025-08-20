# Quick Deploy Guide

## Step 1: Setup AWS Credentials
```bash
# Install AWS CLI
pip install awscli boto3

# Configure credentials
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Region (e.g., us-east-1)
- Output format: json

## Step 2: Get Weather API Key
1. Go to https://openweathermap.org/api
2. Sign up and get your free API key
3. Set environment variable:
```bash
set WEATHER_API_KEY=your_actual_api_key_here
```

## Step 3: Deploy
```bash
cd bedrock-agent
python deploy.py
```

## Step 4: Test
Go to AWS Console > Bedrock > Agents and test your weather agent!