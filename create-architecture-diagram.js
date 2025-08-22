const AWS = require('aws-sdk');
const fs = require('fs');

// Configure AWS
AWS.config.update({ region: 'us-east-1' });

async function generateArchitectureDiagram() {
  const resources = {
    cognito: 'Amazon Cognito (Authentication)',
    bedrock: 'Amazon Bedrock (AI Agents)',
    lambda: 'AWS Lambda (Serverless Functions)',
    react: 'React Frontend (Amplify Hosting)'
  };

  const mermaidDiagram = `
graph TB
    User[👤 User] --> React[📱 React App<br/>Amplify Hosting]
    React --> Cognito[🔐 Amazon Cognito<br/>Authentication]
    React --> ProductAgent[🤖 Product Opportunity Agent<br/>Bedrock]
    React --> WeatherAgent[🌤️ Weather Agent<br/>Bedrock]
    
    ProductAgent --> Lambda1[⚡ Lambda Functions<br/>DCC Analysis]
    WeatherAgent --> Lambda2[⚡ Lambda Functions<br/>Weather Data]
    
    Lambda1 --> Bedrock[🧠 Amazon Bedrock<br/>Claude 3 Haiku]
    Lambda2 --> Bedrock
    
    style User fill:#e1f5fe
    style React fill:#f3e5f5
    style Cognito fill:#fff3e0
    style ProductAgent fill:#e8f5e8
    style WeatherAgent fill:#e8f5e8
    style Lambda1 fill:#fff8e1
    style Lambda2 fill:#fff8e1
    style Bedrock fill:#fce4ec
  `;

  fs.writeFileSync('architecture-diagram.md', mermaidDiagram);
  console.log('Architecture diagram created: architecture-diagram.md');
  console.log('View at: https://mermaid.live/ or in VS Code with Mermaid extension');
}

generateArchitectureDiagram();