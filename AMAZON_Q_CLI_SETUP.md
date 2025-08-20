# Amazon Q CLI Setup Guide

## Current Status
Amazon Q CLI with MCP support is not yet publicly available through standard package managers (pip/npm).

## Alternative Approaches

### Option 1: Manual Installation (When Available)
```bash
# Check AWS documentation for latest installation method
# The CLI may be available through:
# - AWS installer
# - Direct download from AWS
# - Beta/preview program
```

### Option 2: Use AWS CLI with Bedrock
```bash
# Test Bedrock agent directly
aws bedrock-agent invoke-agent \
  --agent-id "your-agent-id" \
  --agent-alias-id "TSTALIASID" \
  --session-id "test-session" \
  --input-text "What's the weather in New York?"
```

### Option 3: Create Architecture Diagram Manually

#### Using Draw.io (Recommended)
1. Go to https://app.diagrams.net/
2. Create new diagram
3. Use AWS architecture icons
4. Follow the text diagram in `ARCHITECTURE.md`

#### Using AWS Architecture Icons
1. Download AWS Architecture Icons from AWS
2. Use tools like Lucidchart, Visio, or PowerPoint
3. Create diagram based on our architecture description

## Architecture Components to Include

### Frontend Layer
- Users → CloudFront → S3 → React App

### Authentication Layer  
- Cognito User Pool (us-east-1_liYtIs82R)
- IAM Role (Cognito_WeatherAppAuth_Role)

### AI Services Layer
- Bedrock Agent (Weather Assistant)
- Lambda Function (weather-function)

### External Services
- OpenWeatherMap API

## Next Steps
1. Monitor AWS announcements for Q CLI availability
2. Use alternative diagramming tools for now
3. Consider using AWS Well-Architected Tool for architecture review