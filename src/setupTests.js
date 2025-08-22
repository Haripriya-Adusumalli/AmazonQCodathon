// jest-dom adds custom jest matchers for asserting on DOM nodes.
import '@testing-library/jest-dom';

// Mock AWS SDK
jest.mock('@aws-sdk/client-bedrock-agent-runtime', () => ({
  BedrockAgentRuntimeClient: jest.fn().mockImplementation(() => ({
    send: jest.fn().mockResolvedValue({
      completion: [
        {
          chunk: {
            bytes: new TextEncoder().encode('Mock response from agent')
          }
        }
      ]
    })
  })),
  InvokeAgentCommand: jest.fn()
}));

// Mock Amplify
jest.mock('aws-amplify/auth', () => ({
  fetchAuthSession: jest.fn().mockResolvedValue({
    credentials: {
      accessKeyId: 'mock-access-key',
      secretAccessKey: 'mock-secret-key',
      sessionToken: 'mock-session-token'
    }
  })
}));

// Mock console methods to reduce noise in tests
global.console = {
  ...console,
  log: jest.fn(),
  warn: jest.fn(),
  error: jest.fn()
};