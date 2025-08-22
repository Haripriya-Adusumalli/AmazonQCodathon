const { spawn } = require('child_process');

// Start AWS Diagram MCP Server
const mcpServer = spawn('npx', ['-y', '@aws/aws-diagram-mcp-server'], {
  stdio: ['pipe', 'pipe', 'pipe']
});

// Basic MCP communication
mcpServer.stdout.on('data', (data) => {
  console.log('MCP Output:', data.toString());
});

// Send MCP request to list AWS resources
const request = {
  jsonrpc: "2.0",
  id: 1,
  method: "tools/list"
};

mcpServer.stdin.write(JSON.stringify(request) + '\n');