const { spawn } = require('child_process');

const mcpServer = spawn('npx', ['-y', '@aws/aws-diagram-mcp-server'], {
  stdio: ['pipe', 'pipe', 'pipe']
});

let responseBuffer = '';

mcpServer.stdout.on('data', (data) => {
  responseBuffer += data.toString();
  
  // Process complete JSON responses
  const lines = responseBuffer.split('\n');
  responseBuffer = lines.pop(); // Keep incomplete line
  
  lines.forEach(line => {
    if (line.trim()) {
      try {
        const response = JSON.parse(line);
        console.log('Response:', JSON.stringify(response, null, 2));
      } catch (e) {
        console.log('Raw output:', line);
      }
    }
  });
});

// Initialize MCP
const init = {
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "diagram-generator", version: "1.0.0" }
  }
};

// Generate diagram for your AWS resources
const generateDiagram = {
  jsonrpc: "2.0",
  id: 2,
  method: "tools/call",
  params: {
    name: "generate_aws_architecture_diagram",
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