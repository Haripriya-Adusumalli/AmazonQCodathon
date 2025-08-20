# React App with Amazon Cognito Authentication

## Overview
A modern React application featuring Amazon Cognito authentication with a clean, gradient-styled UI. Users can sign up, sign in, reset passwords, and access a protected dashboard.

## Features
- ✅ Amazon Cognito User Pool authentication
- ✅ Email-based user registration and login
- ✅ Password reset functionality
- ✅ Protected dashboard route
- ✅ Modern gradient UI design
- ✅ Responsive layout

## Architecture

### Frontend Components
- **App.js** - Main application component with Amplify Authenticator
- **Dashboard.js** - Protected dashboard component for authenticated users
- **aws-config.js** - AWS Cognito configuration
- **App.css** - Styling with gradient backgrounds

### AWS Services
- **Amazon Cognito User Pool** - User authentication and management
- **User Pool ID**: `us-east-1_liYtIs82R`
- **Client ID**: `5gjbh0bueph4233e711bmukh6c`

## Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- AWS Account
- AWS CLI configured

### Quick Start
```bash
# Clone and install dependencies
npm install

# Start the application
npm start
```

### AWS Configuration
The application is pre-configured with:
- **Region**: us-east-1
- **User Pool**: ReactAppUserPool
- **Authentication**: Email-based with verification

## User Authentication Flow

### Sign Up Process
1. User enters email and password
2. Cognito sends verification code to email
3. User enters verification code
4. Account is activated

### Sign In Process
1. User enters email and password
2. Cognito validates credentials
3. User is redirected to dashboard

### Password Reset
1. User clicks "Forgot Password"
2. Enters email address
3. Receives reset code via email
4. Creates new password

## File Structure
```
AQCodathon/
├── src/
│   ├── App.js              # Main app component
│   ├── App.css             # Styling
│   ├── Dashboard.js        # Protected dashboard
│   ├── aws-config.js       # AWS configuration
│   └── index.js            # React entry point
├── public/
│   └── index.html          # HTML template
├── bedrock-agent/          # Bedrock weather agent
├── package.json            # Dependencies
├── setup-cognito.py        # Cognito setup script
└── README.md               # Basic setup guide
```

## Styling & UI

### Design System
- **Primary Colors**: Blue gradient (#667eea to #764ba2)
- **Typography**: Segoe UI font family
- **Components**: Clean white cards with subtle shadows
- **Layout**: Centered, responsive design

### CSS Classes
- `.app` - Main container with gradient background
- `.dashboard` - Dashboard card styling
- `.logout-btn` - Sign out button styling
- `[data-amplify-authenticator]` - Amplify component overrides

## Security Features

### Password Policy
- Minimum 8 characters
- No complexity requirements (configurable)
- Email verification required

### Authentication Methods
- Email + Password
- Admin authentication flows enabled
- No client secret (suitable for web apps)

## Deployment

### Local Development
```bash
npm start
```
Application runs on http://localhost:3000

### Production Build
```bash
npm run build
```
Creates optimized build in `build/` directory

## Troubleshooting

### Common Issues
1. **Port 3000 occupied**: Use `set PORT=3002 && npm start`
2. **AWS credentials**: Run `aws configure` to set up credentials
3. **Module not found**: Run `npm install` to install dependencies

### Error Messages
- **"Module not found: aws-amplify"**: Run `npm install aws-amplify @aws-amplify/ui-react`
- **"AWS credentials not configured"**: Run `aws configure` with your access keys

## Additional Features

### Bedrock Weather Agent
Located in `bedrock-agent/` directory:
- Lambda function for weather data retrieval
- OpenAPI schema for weather API
- Deployment script for AWS Bedrock

## Support
For issues or questions:
1. Check AWS Cognito console for user pool status
2. Verify AWS credentials are configured
3. Ensure all npm dependencies are installed
4. Check browser console for detailed error messages