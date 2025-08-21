# Product Opportunity Recommendation System

A comprehensive AI-powered system that identifies high-potential product opportunities using DCC (Demand + Competition + Capability) analysis.

## 🏗️ Architecture Overview

### Core Components

1. **Orchestrator Agent** - Main coordinator that routes queries and merges insights
2. **Domain Agents** - Specialized agents for different analysis areas:
   - MarketDemand Agent - Google Trends, NewsAPI, Reddit analysis
   - CompetitorScan Agent - Amazon/eBay product analysis
   - CapabilityMatch Agent - Internal readiness assessment via Q Business
   - PricingIntel Agent - Review mining and pain-point analysis
   - FeatureGap Agent - Differentiation strategy recommendations

### 📊 DCC Scoring Model

For each product opportunity:

```
DCC Score = (Demand × 0.45) + ((100 - Competition) × 0.30) + (Capability × 0.25)
```

- **Demand Score (0-100)**: Market interest, trends, momentum
- **Competition Score (0-100)**: Market saturation (lower = better opportunity)  
- **Capability Score (0-100)**: Internal readiness to execute

## 🚀 Quick Deployment

### 1. Deploy the Agent
```bash
cd bedrock-agent/product-opportunity-agent
python simple-deploy.py
```

### 2. Update React Configuration
Copy the agent ID and alias ID from the deployment output to `src/aws-config.js`:

```javascript
export const productOpportunityConfig = {
  agentId: 'YOUR_AGENT_ID',
  aliasId: 'YOUR_ALIAS_ID', 
  region: 'us-east-1'
};
```

### 3. Run the Application
```bash
npm start
```

## 💡 Usage Examples

Try these queries in the Product Opportunity Analyzer:

- "Analyze smart water bottle opportunity in India"
- "What's the potential for eco-friendly phone cases?"
- "Should we launch a fitness tracking app for seniors?"
- "Evaluate the market for AI-powered study tools"

## 🔧 Advanced Setup (Full System)

For production deployment with all domain agents and APIs:

1. **Set up API Keys**:
   - Google Trends API
   - NewsAPI key
   - Reddit API credentials
   - Amazon Product Advertising API

2. **Deploy Lambda Functions**:
   ```bash
   python deploy-product-agents.py
   ```

3. **Configure Q Business Integration** for internal capability analysis

## 📈 Features

- **Real-time Market Analysis** - Live trend data and competitive intelligence
- **DCC Scoring Dashboard** - Visual breakdown of opportunity scores
- **Actionable Recommendations** - Specific next steps and differentiation strategies
- **Risk Assessment** - Capability gaps and mitigation strategies
- **Interactive Chat Interface** - Natural language product opportunity queries

## 🛠️ Technology Stack

- **Frontend**: React 18, AWS Amplify
- **Backend**: Amazon Bedrock Agents, AWS Lambda
- **APIs**: Google Trends, NewsAPI, Amazon Product API
- **Storage**: DynamoDB for analysis caching
- **Auth**: Amazon Cognito
- **AI**: Claude 3 Haiku via Bedrock

## 📋 Next Steps

1. Deploy the basic agent using `simple-deploy.py`
2. Test with sample product queries
3. Integrate real API data sources for production
4. Set up Q Business for internal capability matching
5. Add Slack/Jira integration for workflow automation