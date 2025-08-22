const { spawn } = require('child_process');

async function generateDiagram() {
  return new Promise((resolve, reject) => {
    const mcpServer = spawn('node', ['aws-diagram-mcp-server.js'], {
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let responses = [];
    
    mcpServer.stdout.on('data', (data) => {
      const lines = data.toString().split('\n').filter(line => line.trim());
      lines.forEach(line => {
        try {
          const response = JSON.parse(line);
          responses.push(response);
          if (response.id === 2) {
            console.log('\n=== AWS ARCHITECTURE DIAGRAM ===');
            console.log(response.result.content[0].text);
            mcpServer.kill();
            resolve(response);
          }
        } catch (e) {
          // Ignore non-JSON lines
        }
      });
    });

    mcpServer.stderr.on('data', (data) => {
      console.error('Error:', data.toString());
    });

    // Initialize
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

    // Generate diagram
    const generateCmd = {
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
        mcpServer.stdin.write(JSON.stringify(generateCmd) + '\n');
      }, 1000);
    }, 500);

    setTimeout(() => {
      mcpServer.kill();
      reject(new Error('Timeout'));
    }, 10000);
  });
}

generateDiagram().catch(console.error);