# Bedrock Weather Agent

A Bedrock agent that provides current weather data for cities using OpenWeatherMap API.

## Setup

1. **Get OpenWeatherMap API Key**
   - Sign up at https://openweathermap.org/api
   - Get your free API key

2. **Update Configuration**
   - Replace `YOUR_OPENWEATHER_API_KEY` in `deploy.py` with your actual API key

3. **Deploy**
   ```bash
   pip install boto3
   python deploy.py
   ```

## Usage

The agent can respond to queries like:
- "What's the weather in New York?"
- "Tell me the current weather in London"
- "How's the weather in Tokyo today?"

## Files

- `lambda/weather-function.py` - Lambda function to fetch weather data
- `agent-schema.json` - OpenAPI schema for the weather API
- `deploy.py` - Deployment script for the Bedrock agent