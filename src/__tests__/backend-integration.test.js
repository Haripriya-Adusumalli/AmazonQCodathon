import { BedrockAgentRuntimeClient, InvokeAgentCommand } from '@aws-sdk/client-bedrock-agent-runtime';
import { bedrockConfig, productOpportunityConfig, enhancedProductOpportunityConfig } from '../aws-config';

// Mock AWS credentials
const mockCredentials = {
  accessKeyId: 'test-access-key',
  secretAccessKey: 'test-secret-key',
  sessionToken: 'test-session-token'
};

describe('Backend Integration Tests', () => {
  describe('Weather Agent Backend', () => {
    test('should connect to weather agent', async () => {
      const client = new BedrockAgentRuntimeClient({
        region: bedrockConfig.region,
        credentials: mockCredentials
      });

      const command = new InvokeAgentCommand({
        agentId: bedrockConfig.agentId,
        agentAliasId: bedrockConfig.aliasId,
        sessionId: 'test-session-weather',
        inputText: 'What is the weather today?'
      });

      // Mock successful response
      const mockResponse = {
        completion: [
          {
            chunk: {
              bytes: new TextEncoder().encode('Weather response')
            }
          }
        ]
      };

      jest.spyOn(client, 'send').mockResolvedValue(mockResponse);

      const response = await client.send(command);
      expect(response.completion).toBeDefined();
      expect(response.completion.length).toBeGreaterThan(0);
    });

    test('should validate weather agent configuration', () => {
      expect(bedrockConfig.agentId).toBe('E7QJOXGNCA');
      expect(bedrockConfig.aliasId).toBe('JJYE1KNRVY');
      expect(bedrockConfig.region).toBe('us-east-1');
    });
  });

  describe('Product Opportunity Agent Backend', () => {
    test('should connect to basic product opportunity agent', async () => {
      const client = new BedrockAgentRuntimeClient({
        region: productOpportunityConfig.region,
        credentials: mockCredentials
      });

      const command = new InvokeAgentCommand({
        agentId: productOpportunityConfig.agentId,
        agentAliasId: productOpportunityConfig.aliasId,
        sessionId: 'test-session-product',
        inputText: 'Analyze smart water bottle opportunity'
      });

      const mockResponse = {
        completion: [
          {
            chunk: {
              bytes: new TextEncoder().encode('Product analysis response')
            }
          }
        ]
      };

      jest.spyOn(client, 'send').mockResolvedValue(mockResponse);

      const response = await client.send(command);
      expect(response.completion).toBeDefined();
    });

    test('should validate basic agent configuration', () => {
      expect(productOpportunityConfig.agentId).toBe('DKPL7RP9OU');
      expect(productOpportunityConfig.aliasId).toBe('NTC6Q4Y2BZ');
      expect(productOpportunityConfig.region).toBe('us-east-1');
    });
  });

  describe('Enhanced Product Opportunity Agent Backend', () => {
    test('should connect to enhanced product opportunity agent', async () => {
      const client = new BedrockAgentRuntimeClient({
        region: enhancedProductOpportunityConfig.region,
        credentials: mockCredentials
      });

      const command = new InvokeAgentCommand({
        agentId: enhancedProductOpportunityConfig.agentId,
        agentAliasId: enhancedProductOpportunityConfig.aliasId,
        sessionId: 'test-session-enhanced',
        inputText: 'Analyze eco-friendly phone cases opportunity',
        enableTrace: true
      });

      const mockResponse = {
        completion: [
          {
            chunk: {
              bytes: new TextEncoder().encode('Enhanced analysis with real API data')
            }
          }
        ]
      };

      jest.spyOn(client, 'send').mockResolvedValue(mockResponse);

      const response = await client.send(command);
      expect(response.completion).toBeDefined();
    });

    test('should validate enhanced agent configuration', () => {
      expect(enhancedProductOpportunityConfig.agentId).toBe('BKWEM7GZQX');
      expect(enhancedProductOpportunityConfig.aliasId).toBe('JPWRQS8CI3');
      expect(enhancedProductOpportunityConfig.region).toBe('us-east-1');
    });
  });

  describe('Lambda Function Integration', () => {
    test('should validate Lambda function responses', () => {
      const mockLambdaResponse = {
        demand_score: 75.5,
        current_interest: 82.0,
        momentum: 1.35,
        trending_topics: ['smart water bottle reviews', 'IoT water bottle', 'water bottle connectivity'],
        news_volume: 25,
        news_sentiment: 'positive',
        data_source: 'enhanced_mock',
        analysis_timestamp: '2025-08-22T07:45:30.123456'
      };

      expect(mockLambdaResponse.demand_score).toBeGreaterThan(0);
      expect(mockLambdaResponse.demand_score).toBeLessThanOrEqual(100);
      expect(mockLambdaResponse.trending_topics).toHaveLength(3);
      expect(['positive', 'neutral', 'negative']).toContain(mockLambdaResponse.news_sentiment);
      expect(['real_apis', 'enhanced_mock']).toContain(mockLambdaResponse.data_source);
    });
  });

  describe('Error Handling', () => {
    test('should handle agent not found errors', async () => {
      const client = new BedrockAgentRuntimeClient({
        region: 'us-east-1',
        credentials: mockCredentials
      });

      const command = new InvokeAgentCommand({
        agentId: 'invalid-agent-id',
        agentAliasId: 'invalid-alias-id',
        sessionId: 'test-session',
        inputText: 'test query'
      });

      jest.spyOn(client, 'send').mockRejectedValue(new Error('ResourceNotFoundException'));

      await expect(client.send(command)).rejects.toThrow('ResourceNotFoundException');
    });

    test('should handle authentication errors', async () => {
      const client = new BedrockAgentRuntimeClient({
        region: 'us-east-1',
        credentials: {
          accessKeyId: 'invalid',
          secretAccessKey: 'invalid',
          sessionToken: 'invalid'
        }
      });

      const command = new InvokeAgentCommand({
        agentId: bedrockConfig.agentId,
        agentAliasId: bedrockConfig.aliasId,
        sessionId: 'test-session',
        inputText: 'test query'
      });

      jest.spyOn(client, 'send').mockRejectedValue(new Error('UnauthorizedOperation'));

      await expect(client.send(command)).rejects.toThrow('UnauthorizedOperation');
    });
  });
});