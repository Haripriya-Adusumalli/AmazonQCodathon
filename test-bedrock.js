const { BedrockAgentRuntimeClient, InvokeAgentCommand } = require('@aws-sdk/client-bedrock-agent-runtime');

async function testBedrockAgent() {
  try {
    const client = new BedrockAgentRuntimeClient({
      region: 'us-east-1'
    });

    const command = new InvokeAgentCommand({
      agentId: 'E7QJOXGNCA',
      agentAliasId: 'JJYE1KNRVY',
      sessionId: `test-session-${Date.now()}`,
      inputText: 'Hello! Can you tell me about different types of weather?'
    });

    console.log('Testing Bedrock agent...');
    const response = await client.send(command);
    
    let fullResponse = '';
    if (response.completion) {
      for await (const chunk of response.completion) {
        if (chunk.chunk?.bytes) {
          const text = new TextDecoder().decode(chunk.chunk.bytes);
          fullResponse += text;
        }
      }
    }

    console.log('Agent Response:', fullResponse);
    
  } catch (error) {
    console.error('Error testing Bedrock agent:', error.message);
  }
}

testBedrockAgent();