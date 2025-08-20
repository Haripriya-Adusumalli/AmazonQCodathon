# Deployment Guide

## Local Development Setup

### 1. Prerequisites
- Node.js 14+ installed
- AWS Account with appropriate permissions
- Git (optional)

### 2. Installation Steps
```bash
# Navigate to project directory
cd AQCodathon

# Install dependencies
npm install

# Install AWS CLI (if not already installed)
pip install awscli boto3
```

### 3. AWS Configuration
```bash
# Configure AWS credentials
aws configure

# Set output format to JSON
aws configure set output json

# Verify connection
aws sts get-caller-identity
```

### 4. Cognito Setup
```bash
# Run automated Cognito setup
python setup-cognito.py
```

### 5. Start Application
```bash
# Start development server
npm start

# If port 3000 is occupied
set PORT=3002 && npm start
```

## Production Deployment

### AWS Amplify Hosting

#### Option 1: Amplify Console
1. Go to AWS Amplify Console
2. Click "New app" → "Host web app"
3. Connect your Git repository
4. Configure build settings:
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

#### Option 2: Amplify CLI
```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize Amplify project
amplify init

# Add hosting
amplify add hosting

# Deploy
amplify publish
```

### Static Hosting (S3 + CloudFront)

#### 1. Build Application
```bash
npm run build
```

#### 2. Create S3 Bucket
```bash
aws s3 mb s3://your-app-bucket-name
```

#### 3. Upload Build Files
```bash
aws s3 sync build/ s3://your-app-bucket-name --delete
```

#### 4. Configure S3 for Static Hosting
```bash
aws s3 website s3://your-app-bucket-name --index-document index.html
```

## Environment Configuration

### Development Environment
```bash
# .env.development
REACT_APP_AWS_REGION=us-east-1
REACT_APP_USER_POOL_ID=us-east-1_liYtIs82R
REACT_APP_USER_POOL_CLIENT_ID=5gjbh0bueph4233e711bmukh6c
```

### Production Environment
```bash
# .env.production
REACT_APP_AWS_REGION=us-east-1
REACT_APP_USER_POOL_ID=us-east-1_liYtIs82R
REACT_APP_USER_POOL_CLIENT_ID=5gjbh0bueph4233e711bmukh6c
```

## Bedrock Agent Deployment

### 1. Get OpenWeatherMap API Key
- Sign up at https://openweathermap.org/api
- Get your free API key

### 2. Set Environment Variable
```bash
set WEATHER_API_KEY=your_actual_api_key
```

### 3. Deploy Bedrock Agent
```bash
cd bedrock-agent
python deploy.py
```

## Monitoring & Logging

### CloudWatch Integration
```javascript
// Add to aws-config.js for logging
export const awsConfig = {
  Auth: {
    Cognito: {
      userPoolId: 'us-east-1_liYtIs82R',
      userPoolClientId: '5gjbh0bueph4233e711bmukh6c',
      region: 'us-east-1'
    }
  },
  Analytics: {
    AWSPinpoint: {
      appId: 'your-pinpoint-app-id',
      region: 'us-east-1'
    }
  }
};
```

## Security Considerations

### HTTPS Configuration
- Always use HTTPS in production
- Configure SSL certificates
- Enable HSTS headers

### CORS Configuration
```javascript
// For API Gateway or custom APIs
const corsConfig = {
  origin: ['https://yourdomain.com'],
  credentials: true
};
```

### Content Security Policy
```html
<!-- Add to public/index.html -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline'; 
               style-src 'self' 'unsafe-inline';">
```

## Troubleshooting Deployment

### Common Issues
1. **Build Failures**: Check Node.js version compatibility
2. **AWS Permissions**: Ensure IAM user has required permissions
3. **CORS Errors**: Configure API Gateway CORS settings
4. **Authentication Errors**: Verify Cognito configuration

### Debug Commands
```bash
# Check build output
npm run build

# Test production build locally
npx serve -s build

# Check AWS configuration
aws configure list

# Verify Cognito setup
aws cognito-idp describe-user-pool --user-pool-id us-east-1_liYtIs82R
```

## Performance Optimization

### Build Optimization
```bash
# Analyze bundle size
npm install -g webpack-bundle-analyzer
npx webpack-bundle-analyzer build/static/js/*.js
```

### Caching Strategy
- Enable CloudFront caching
- Set appropriate cache headers
- Use service workers for offline functionality

## Rollback Strategy

### Quick Rollback
```bash
# Revert to previous Amplify deployment
amplify env checkout previous

# Or restore from S3 backup
aws s3 sync s3://backup-bucket/previous-version/ s3://your-app-bucket-name/
```