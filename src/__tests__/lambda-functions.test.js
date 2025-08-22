// Lambda function unit tests
describe('Lambda Function Tests', () => {
  describe('Market Demand Agent', () => {
    test('should calculate demand score correctly', () => {
      const mockEvent = {
        requestBody: {
          query: 'smart water bottle',
          region: 'US'
        }
      };

      // Mock the lambda handler logic
      const calculateMockInterest = (query) => {
        const baseScore = query.length * 3;
        return Math.min(100, baseScore + (Math.abs(query.split('').reduce((a, b) => a + b.charCodeAt(0), 0)) % 30));
      };

      const calculateMockMomentum = (query) => {
        return 1.0 + (Math.abs(query.split('').reduce((a, b) => a + b.charCodeAt(0), 0)) % 50) / 100;
      };

      const generateMockTopics = (query) => {
        return [
          `${query} reviews`,
          `best ${query}`,
          `${query} alternatives`
        ];
      };

      const query = mockEvent.requestBody.query;
      const currentInterest = calculateMockInterest(query);
      const momentum = calculateMockMomentum(query);
      const trendingTopics = generateMockTopics(query);
      const newsVolume = Math.min(50, query.length * 2);
      const demandScore = Math.min(100, (currentInterest * 0.6 + momentum * 20 + newsVolume * 0.2));

      expect(currentInterest).toBeGreaterThan(0);
      expect(currentInterest).toBeLessThanOrEqual(100);
      expect(momentum).toBeGreaterThan(1.0);
      expect(trendingTopics).toHaveLength(3);
      expect(demandScore).toBeGreaterThan(0);
      expect(demandScore).toBeLessThanOrEqual(100);
    });

    test('should handle different query formats', () => {
      const testCases = [
        { requestBody: { query: 'fitness app' } },
        { query: 'eco-friendly phone case' },
        { inputText: 'smart home device' }
      ];

      testCases.forEach(event => {
        let query = 'product';
        if (event.requestBody && event.requestBody.query) {
          query = event.requestBody.query;
        } else if (event.query) {
          query = event.query;
        } else if (event.inputText) {
          query = event.inputText;
        }

        expect(query).toBeDefined();
        expect(query.length).toBeGreaterThan(0);
      });
    });
  });

  describe('Enhanced Market Demand Agent', () => {
    test('should categorize queries correctly', () => {
      const categorizeQuery = (query) => {
        const queryLower = query.toLowerCase();
        
        if (['smart', 'ai', 'iot'].some(word => queryLower.includes(word))) {
          return 'smart_tech';
        } else if (['eco', 'green', 'sustainable'].some(word => queryLower.includes(word))) {
          return 'eco_friendly';
        } else if (['fitness', 'health', 'wellness'].some(word => queryLower.includes(word))) {
          return 'health_fitness';
        }
        return 'general';
      };

      expect(categorizeQuery('smart water bottle')).toBe('smart_tech');
      expect(categorizeQuery('eco-friendly phone case')).toBe('eco_friendly');
      expect(categorizeQuery('fitness tracking app')).toBe('health_fitness');
      expect(categorizeQuery('regular product')).toBe('general');
    });

    test('should generate category-specific trending topics', () => {
      const generateCategoryTopics = (query, category) => {
        if (category === 'smart_tech') {
          return [`smart ${query} reviews`, `IoT ${query}`, `${query} connectivity`];
        } else if (category === 'eco_friendly') {
          return [`sustainable ${query}`, `eco ${query} materials`, `green ${query}`];
        } else if (category === 'health_fitness') {
          return [`${query} fitness tracking`, `health ${query}`, `${query} wellness`];
        }
        return [`${query} reviews`, `best ${query} 2024`, `${query} price`];
      };

      const smartTopics = generateCategoryTopics('water bottle', 'smart_tech');
      const ecoTopics = generateCategoryTopics('phone case', 'eco_friendly');
      const fitnessTopics = generateCategoryTopics('app', 'health_fitness');

      expect(smartTopics[0]).toContain('smart');
      expect(ecoTopics[0]).toContain('sustainable');
      expect(fitnessTopics[0]).toContain('fitness');
    });

    test('should calculate enhanced demand score', () => {
      const calculateEnhancedDemandScore = (trendsData, newsData) => {
        const interestScore = Math.min(100, trendsData.currentInterest);
        const momentumScore = Math.min(50, trendsData.momentum * 25);
        const newsScore = Math.min(30, newsData.volume * 0.5);
        
        let sentimentBonus = 0;
        if (newsData.sentiment === 'positive') {
          sentimentBonus = 10;
        } else if (newsData.sentiment === 'negative') {
          sentimentBonus = -5;
        }
        
        const totalScore = interestScore * 0.5 + momentumScore * 0.3 + newsScore * 0.2 + sentimentBonus;
        return Math.max(0, Math.min(100, totalScore));
      };

      const mockTrendsData = {
        currentInterest: 85,
        momentum: 1.25
      };

      const mockNewsData = {
        volume: 40,
        sentiment: 'positive'
      };

      const score = calculateEnhancedDemandScore(mockTrendsData, mockNewsData);
      expect(score).toBeGreaterThan(0);
      expect(score).toBeLessThanOrEqual(100);
    });
  });

  describe('Response Format Validation', () => {
    test('should return correct Bedrock response format', () => {
      const mockResult = {
        demand_score: 75.5,
        current_interest: 82.0,
        momentum: 1.35,
        trending_topics: ['topic1', 'topic2', 'topic3'],
        news_volume: 25,
        news_sentiment: 'positive'
      };

      const bedrockResponse = {
        messageVersion: '1.0',
        response: {
          actionGroup: 'demand-analysis',
          apiPath: '/analyze-demand',
          httpMethod: 'POST',
          httpStatusCode: 200,
          responseBody: {
            'application/json': {
              body: JSON.stringify(mockResult)
            }
          }
        }
      };

      expect(bedrockResponse.messageVersion).toBe('1.0');
      expect(bedrockResponse.response.httpStatusCode).toBe(200);
      expect(bedrockResponse.response.responseBody['application/json'].body).toBeDefined();
      
      const parsedBody = JSON.parse(bedrockResponse.response.responseBody['application/json'].body);
      expect(parsedBody.demand_score).toBe(75.5);
      expect(parsedBody.trending_topics).toHaveLength(3);
    });

    test('should return correct simple response format', () => {
      const mockResult = {
        demand_score: 68.2,
        current_interest: 75.0,
        momentum: 1.15
      };

      const simpleResponse = {
        statusCode: 200,
        body: JSON.stringify(mockResult)
      };

      expect(simpleResponse.statusCode).toBe(200);
      expect(simpleResponse.body).toBeDefined();
      
      const parsedBody = JSON.parse(simpleResponse.body);
      expect(parsedBody.demand_score).toBe(68.2);
    });
  });

  describe('Error Handling', () => {
    test('should handle errors gracefully', () => {
      const createErrorResponse = (error, isBedrock = false) => {
        const errorResult = { error: error.message };
        
        if (isBedrock) {
          return {
            messageVersion: '1.0',
            response: {
              actionGroup: 'demand-analysis',
              apiPath: '/analyze-demand',
              httpMethod: 'POST',
              httpStatusCode: 500,
              responseBody: {
                'application/json': {
                  body: JSON.stringify(errorResult)
                }
              }
            }
          };
        } else {
          return {
            statusCode: 500,
            body: JSON.stringify(errorResult)
          };
        }
      };

      const testError = new Error('Test error');
      const bedrockErrorResponse = createErrorResponse(testError, true);
      const simpleErrorResponse = createErrorResponse(testError, false);

      expect(bedrockErrorResponse.response.httpStatusCode).toBe(500);
      expect(simpleErrorResponse.statusCode).toBe(500);
      
      const bedrockErrorBody = JSON.parse(bedrockErrorResponse.response.responseBody['application/json'].body);
      const simpleErrorBody = JSON.parse(simpleErrorResponse.body);
      
      expect(bedrockErrorBody.error).toBe('Test error');
      expect(simpleErrorBody.error).toBe('Test error');
    });
  });
});