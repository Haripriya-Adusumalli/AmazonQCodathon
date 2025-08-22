const { spawn } = require('child_process');

const mcpServer = spawn('node', ['aws-diagram-mcp-server.js'], {
  stdio: ['pipe', 'pipe', 'pipe']
});

let buffer = '';

mcpServer.stdout.on('data', (data) => {
  buffer += data.toString();
  console.log('MCP Response:', buffer);
});

mcpServer.stderr.on('data', (data) => {
  console.error('MCP Error:', data.toString());
});

// Initialize MCP
const init = {
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "aws-diagram-client", version: "1.0.0" }
  }
};

// Generate diagram
const generateDiagram = {
  jsonrpc: "2.0",
  id: 2,
  method: "tools/call",
  params: {
    name: "generate_aws_diagram",
    arguments: {
      region: "us-east-1",
      title: "Product Opportunity Recommendation System"
    }
  }
};

setTimeout(() => {
  mcpServer.stdin.write(JSON.stringify(init) + '\n');
  setTimeout(() => {
    mcpServer.stdin.write(JSON.stringify(generateDiagram) + '\n');
  }, 1000);
}, 500);