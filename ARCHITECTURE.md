# AWS Architecture Diagram

## Text-Based Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                           USERS                                 │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ CloudFront  │◄───┤     S3      │◄───┤   React App         │  │
│  │    CDN      │    │   Static    │    │ (Cognito Auth UI)   │  │
│  │             │    │  Hosting    │    │                     │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 AUTHENTICATION LAYER                           │
│  ┌─────────────────────────────┐    ┌─────────────────────────┐  │
│  │      Cognito User Pool      │    │       IAM Role          │  │
│  │   us-east-1_liYtIs82R      │◄───┤ Cognito_WeatherAppAuth  │  │
│  │                             │    │        _Role            │  │
│  │ • Email Authentication     │    │                         │  │
│  │ • Password Reset           │    │ • bedrock:InvokeAgent   │  │
│  │ • User Registration        │    │ • bedrock:InvokeModel   │  │
│  └─────────────────────────────┘    └─────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI SERVICES LAYER                           │
│  ┌─────────────────────────────┐    ┌─────────────────────────┐  │
│  │      Bedrock Agent          │    │    Lambda Function      │  │
│  │    Weather Assistant        │◄───┤   weather-function      │  │
│  │                             │    │                         │  │
│  │ • Natural Language Query   │    │ • OpenWeatherMap API    │  │
│  │ • Weather Data Processing  │    │ • JSON Response         │  │
│  │ • Claude 3 Sonnet Model    │    │ • Error Handling        │  │
│  └─────────────────────────────┘    └─────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                            │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │              OpenWeatherMap API                             │  │
│  │                                                             │  │
│  │ • Current Weather Data                                      │  │
│  │ • City-based Queries                                        │  │
│  │ • Temperature, Humidity, Wind                               │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **User Access**: Users access the React app via CloudFront CDN
2. **Authentication**: Users sign in through Cognito User Pool
3. **Authorization**: Cognito assumes IAM role with Bedrock permissions
4. **Weather Query**: User asks weather question in natural language
5. **AI Processing**: Bedrock agent processes query using Claude model
6. **Function Invocation**: Agent calls Lambda function for weather data
7. **API Call**: Lambda fetches data from OpenWeatherMap API
8. **Response**: Weather data flows back through the chain to user

## AWS Services Used

- **Amazon Cognito**: User authentication and management
- **Amazon Bedrock**: AI agent for natural language processing
- **AWS Lambda**: Serverless function for weather API integration
- **Amazon S3**: Static website hosting
- **Amazon CloudFront**: Content delivery network
- **AWS IAM**: Identity and access management

## Security Features

- Email-based authentication with verification
- IAM roles with least privilege access
- HTTPS encryption throughout
- API key management for external services

## To Generate Visual Diagram with MCP Server

Follow the AWS blog instructions:
1. Install Amazon Q CLI with MCP support
2. Use the AWS Architecture MCP server
3. Provide this architecture description to generate visual diagram