# API Reference

## AWS Cognito Configuration

### awsConfig Object
```javascript
export const awsConfig = {
  Auth: {
    Cognito: {
      userPoolId: 'us-east-1_liYtIs82R',
      userPoolClientId: '5gjbh0bueph4233e711bmukh6c',
      region: 'us-east-1'
    }
  }
};
```

## React Components

### App Component
```javascript
function App()
```
**Description**: Main application component that wraps the entire app with Amplify Authenticator.

**Returns**: JSX element with Authenticator wrapper

### Dashboard Component
```javascript
function Dashboard({ user, onLogout })
```
**Props**:
- `user` (object): Authenticated user object from Cognito
- `onLogout` (function): Sign out function from Authenticator

**Returns**: JSX element displaying user dashboard

## Amplify Authenticator

### Available Props
- `user.username`: User's username
- `user.signInDetails.loginId`: User's email address
- `signOut()`: Function to sign out user

### Authentication States
- **signIn**: User needs to sign in
- **signUp**: User needs to create account
- **confirmSignUp**: User needs to verify email
- **forgotPassword**: User is resetting password
- **authenticated**: User is signed in

## Cognito User Pool Details

### User Pool Configuration
- **Pool Name**: ReactAppUserPool
- **Username Attributes**: Email
- **Auto Verified Attributes**: Email
- **Password Policy**: Minimum 8 characters

### App Client Configuration
- **Client Name**: ReactAppClient
- **Generate Secret**: False (for web apps)
- **Auth Flows**: ADMIN_NO_SRP_AUTH, USER_PASSWORD_AUTH

## Environment Variables

### Required for Bedrock Agent
```bash
WEATHER_API_KEY=your_openweather_api_key
```

## AWS CLI Commands

### Configure Credentials
```bash
aws configure
aws configure set output json
```

### Verify Configuration
```bash
aws sts get-caller-identity
```

## NPM Scripts

### Available Commands
```json
{
  "start": "react-scripts start",
  "build": "react-scripts build"
}
```

## Dependencies

### Core Dependencies
- `react`: ^18.2.0
- `react-dom`: ^18.2.0
- `aws-amplify`: ^6.0.0
- `@aws-amplify/ui-react`: ^6.0.0

### Development Dependencies
- `react-scripts`: 5.0.1