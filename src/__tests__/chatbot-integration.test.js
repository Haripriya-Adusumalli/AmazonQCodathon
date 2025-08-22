import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Amplify } from 'aws-amplify';
import BedrockChat from '../BedrockChat';
import ProductOpportunityChat from '../ProductOpportunityChat';
import { awsConfig, bedrockConfig, productOpportunityConfig, enhancedProductOpportunityConfig } from '../aws-config';

// Mock AWS SDK
jest.mock('@aws-sdk/client-bedrock-agent-runtime', () => ({
  BedrockAgentRuntimeClient: jest.fn().mockImplementation(() => ({
    send: jest.fn().mockResolvedValue({
      completion: [
        {
          chunk: {
            bytes: new TextEncoder().encode('Test response from weather agent')
          }
        }
      ]
    })
  })),
  InvokeAgentCommand: jest.fn()
}));

// Mock Amplify Auth
jest.mock('aws-amplify/auth', () => ({
  fetchAuthSession: jest.fn().mockResolvedValue({
    credentials: {
      accessKeyId: 'test-access-key',
      secretAccessKey: 'test-secret-key',
      sessionToken: 'test-session-token'
    }
  })
}));

describe('Chatbot Integration Tests', () => {
  beforeAll(() => {
    Amplify.configure(awsConfig);
  });

  describe('Weather Assistant (BedrockChat)', () => {
    test('should render weather chat interface', () => {
      render(<BedrockChat />);
      
      expect(screen.getByText(/Weather Assistant/i)).toBeInTheDocument();
      expect(screen.getByPlaceholderText(/Ask about weather/i)).toBeInTheDocument();
      expect(screen.getByText(/Send/i)).toBeInTheDocument();
    });

    test('should send weather query and receive response', async () => {
      render(<BedrockChat />);
      
      const input = screen.getByPlaceholderText(/Ask about weather/i);
      const sendButton = screen.getByText(/Send/i);
      
      fireEvent.change(input, { target: { value: 'What is the weather today?' } });
      fireEvent.click(sendButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Test response from weather agent/i)).toBeInTheDocument();
      });
    });

    test('should validate agent configuration', () => {
      expect(bedrockConfig.agentId).toBe('E7QJOXGNCA');
      expect(bedrockConfig.aliasId).toBe('JJYE1KNRVY');
      expect(bedrockConfig.region).toBe('us-east-1');
    });
  });

  describe('Product Opportunity Analyzer (Basic)', () => {
    test('should render product opportunity chat interface', () => {
      render(<ProductOpportunityChat enhanced={false} />);
      
      expect(screen.getByText(/Product Opportunity Analyzer/i)).toBeInTheDocument();
      expect(screen.getByPlaceholderText(/Describe your product idea/i)).toBeInTheDocument();
      expect(screen.getByText(/Analyze/i)).toBeInTheDocument();
    });

    test('should display example questions', () => {
      render(<ProductOpportunityChat enhanced={false} />);
      
      expect(screen.getByText(/Analyze smart water bottle opportunity in India/i)).toBeInTheDocument();
      expect(screen.getByText(/What's the potential for eco-friendly phone cases/i)).toBeInTheDocument();
      expect(screen.getByText(/Should we launch a fitness tracking app/i)).toBeInTheDocument();
    });

    test('should validate basic agent configuration', () => {
      expect(productOpportunityConfig.agentId).toBe('DKPL7RP9OU');
      expect(productOpportunityConfig.aliasId).toBe('NTC6Q4Y2BZ');
      expect(productOpportunityConfig.region).toBe('us-east-1');
    });
  });

  describe('Enhanced Product Opportunity Analyzer', () => {
    test('should render enhanced chat interface', () => {
      render(<ProductOpportunityChat enhanced={true} />);
      
      expect(screen.getByText(/Enhanced Product Analyzer/i)).toBeInTheDocument();
      expect(screen.getByText(/Real API Integration/i)).toBeInTheDocument();
      expect(screen.getByText(/Show Logs/i)).toBeInTheDocument();
    });

    test('should validate enhanced agent configuration', () => {
      expect(enhancedProductOpportunityConfig.agentId).toBe('BKWEM7GZQX');
      expect(enhancedProductOpportunityConfig.aliasId).toBe('JPWRQS8CI3');
      expect(enhancedProductOpportunityConfig.region).toBe('us-east-1');
    });
  });

  describe('Error Handling', () => {
    test('should handle authentication errors gracefully', async () => {
      const mockFetchAuthSession = require('aws-amplify/auth').fetchAuthSession;
      mockFetchAuthSession.mockRejectedValueOnce(new Error('Auth failed'));

      render(<BedrockChat />);
      
      const input = screen.getByPlaceholderText(/Ask about weather/i);
      const sendButton = screen.getByText(/Send/i);
      
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.click(sendButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Error: Auth failed/i)).toBeInTheDocument();
      });
    });
  });
});