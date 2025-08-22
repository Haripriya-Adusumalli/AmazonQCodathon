#!/usr/bin/env node

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { CallToolRequestSchema } = require('@modelcontextprotocol/sdk/types.js');
const AWS = require('@aws-sdk/client-bedrock-agent');
const { fromNodeProviderChain } = require('@aws-sdk/credential-providers');

class AWSMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'aws-diagram-server',
        version: '0.1.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
  }

  setupToolHandlers() {
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      switch (request.params.name) {
        case 'generate_aws_diagram':
        case 'generate_aws_architecture_diagram':
          return await this.generateAWSDiagram(request.params.arguments);
        default:
          throw new Error(`Unknown tool: ${request.params.name}`);
      }
    });
  }

  async generateAWSDiagram(args) {
    const { region = 'us-east-1', title = 'AWS Architecture' } = args;
    
    // Scan your actual AWS resources
    const resources = await this.scanAWSResources(region);
    
    const diagram = this.createDiagram(resources, title);
    
    return {
      content: [
        {
          type: 'text',
          text: `AWS Architecture Diagram for ${title}:\n\n${diagram}`
        }
      ]
    };
  }

  async scanAWSResources(region) {
    try {
      const credentials = fromNodeProviderChain();
      const bedrockClient = new AWS.BedrockAgentClient({ 
        region, 
        credentials 
      });
      
      // Get your Bedrock agents
      const agents = await bedrockClient.listAgents({});
      
      return {
        bedrock_agents: agents.agentSummaries || [],
        region
      };
    } catch (error) {
      return { error: error.message, region };
    }
  }

  createDiagram(resources, title) {
    return `
# ${title}

## 🏗️ Architecture with AWS Icons

\`\`\`
    👤 User
     │
     ▼
┌─────────────────┐
│ 📱 React App    │ ◄─── AWS Amplify
│    Frontend     │
└─────────────────┘
     │
     ├─────────────────────┐
     │                     │
     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐
│ 🔐 Amazon       │   │ 🤖 Amazon       │
│    Cognito      │   │    Bedrock      │
│ Authentication  │   │ AI Agents (${resources.bedrock_agents?.length || 0})   │
└─────────────────┘   └─────────────────┘
                           │
                           ▼
                      ┌─────────────────┐
                      │ ⚡ AWS Lambda   │
                      │   Functions     │
                      └─────────────────┘
                           │
                           ▼
                      ┌─────────────────┐
                      │ 🧠 Claude 3     │
                      │    Haiku        │
                      └─────────────────┘
\`\`\`

## 📊 Resource Summary
- 🌍 Region: ${resources.region}
- 🤖 Bedrock Agents: ${resources.bedrock_agents?.length || 0}
- 📱 Frontend: React with Amplify
- 🔐 Auth: Amazon Cognito
- ⚡ Compute: AWS Lambda
- 🧠 AI: Amazon Bedrock + Claude

## 🔍 Discovered Agents:
${resources.bedrock_agents?.map(agent => `🤖 ${agent.agentName} (${agent.agentId})`).join('\n') || '❌ No agents found - check permissions'}
`;
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
  }
}

if (require.main === module) {
  const server = new AWSMCPServer();
  server.run().catch(console.error);
}

module.exports = AWSMCPServer;