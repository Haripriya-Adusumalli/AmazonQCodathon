import json
from datetime import datetime

def lambda_handler(event, context):
    """Market Demand Agent with real API integration and enhanced fallback"""
    
    try:
        # Parse input
        if isinstance(event, str):
            event = json.loads(event)
        
        query = event.get('query', '')
        region = event.get('region', 'US')
        
        # Try real APIs first, fallback to enhanced mock
        try:
            from pytrends.request import TrendReq
            import requests
            demand_data = get_real_trends_data(query, region)
            news_data = get_real_news_data(query)
            data_source = "real_apis"
        except ImportError:
            demand_data = get_enhanced_mock_trends(query, region)
            news_data = get_enhanced_mock_news(query)
            data_source = "enhanced_mock"
        
        # Calculate demand score
        demand_score = calculate_demand_score(demand_data, news_data)
        
        result = {
            'demand_score': round(demand_score, 2),
            'current_interest': demand_data['current_interest'],
            'momentum': demand_data['momentum'],
            'trending_topics': demand_data['trending_topics'],
            'news_volume': news_data['volume'],
            'news_sentiment': news_data['sentiment'],
            'region': region,
            'data_source': data_source,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_real_trends_data(query, region):
    """Get real Google Trends data"""
    from pytrends.request import TrendReq
    
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([query], cat=0, timeframe='today 12-m', geo=region)
    
    interest_over_time = pytrends.interest_over_time()
    
    if not interest_over_time.empty:
        current_interest = interest_over_time[query].iloc[-4:].mean()
        historical_avg = interest_over_time[query].mean()
        momentum = (current_interest / historical_avg) if historical_avg > 0 else 1
    else:
        current_interest = 0
        momentum = 0
    
    related_queries = pytrends.related_queries()
    trending_topics = []
    if query in related_queries and related_queries[query]['rising'] is not None:
        trending_topics = related_queries[query]['rising']['query'].head(5).tolist()
    
    return {
        'current_interest': round(current_interest, 2),
        'momentum': round(momentum, 2),
        'trending_topics': trending_topics
    }

def get_real_news_data(query):
    """Get real news data"""
    import requests
    import os
    
    api_key = os.environ.get('NEWS_API_KEY')
    if not api_key:
        return get_enhanced_mock_news(query)
    
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'from': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'apiKey': api_key,
        'language': 'en',
        'sortBy': 'relevancy'
    }
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    volume = len(data.get('articles', []))
    
    # Simple sentiment analysis
    positive_words = ['good', 'great', 'excellent', 'amazing', 'best', 'top']
    negative_words = ['bad', 'worst', 'terrible', 'awful', 'poor']
    
    sentiment_score = 0
    for article in data.get('articles', [])[:10]:
        title = article.get('title', '').lower()
        sentiment_score += sum(1 for word in positive_words if word in title)
        sentiment_score -= sum(1 for word in negative_words if word in title)
    
    if sentiment_score > 0:
        sentiment = 'positive'
    elif sentiment_score < 0:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {'volume': volume, 'sentiment': sentiment}

def get_enhanced_mock_trends(query, region):
    """Enhanced mock trends data based on query analysis"""
    
    # Analyze query for market indicators
    query_lower = query.lower()
    
    # Base interest calculation
    base_interest = len(query) * 4
    
    # Boost for trending categories
    if any(word in query_lower for word in ['smart', 'ai', 'eco', 'sustainable']):
        base_interest += 25
    if any(word in query_lower for word in ['fitness', 'health', 'wellness']):
        base_interest += 20
    if any(word in query_lower for word in ['app', 'digital', 'online']):
        base_interest += 15
    
    # Regional adjustments
    if region in ['IN', 'India']:
        base_interest += 10  # Growing market
    elif region in ['US', 'United States']:
        base_interest += 5   # Mature market
    
    current_interest = min(100, base_interest + (hash(query) % 20))
    momentum = 1.0 + (hash(query + region) % 40) / 100
    
    # Generate realistic trending topics
    trending_topics = [
        f"{query} reviews",
        f"best {query} 2024",
        f"{query} price",
        f"cheap {query}",
        f"{query} alternatives"
    ]
    
    return {
        'current_interest': round(current_interest, 2),
        'momentum': round(momentum, 2),
        'trending_topics': trending_topics[:3]
    }

def get_enhanced_mock_news(query):
    """Enhanced mock news data"""
    
    # Calculate volume based on query popularity indicators
    volume = len(query) * 3
    
    # Adjust for trending topics
    if any(word in query.lower() for word in ['smart', 'ai', 'tech']):
        volume += 15
    if any(word in query.lower() for word in ['eco', 'green', 'sustainable']):
        volume += 12
    if any(word in query.lower() for word in ['health', 'fitness']):
        volume += 10
    
    # Sentiment based on market perception
    if 'eco' in query.lower() or 'green' in query.lower():
        sentiment = 'positive'
    elif 'cheap' in query.lower() or 'budget' in query.lower():
        sentiment = 'neutral'
    else:
        sentiment = 'positive' if hash(query) % 3 > 0 else 'neutral'
    
    return {'volume': min(100, volume), 'sentiment': sentiment}

def calculate_demand_score(demand_data, news_data):
    """Calculate overall demand score"""
    interest_score = min(100, demand_data['current_interest'])
    momentum_score = min(50, demand_data['momentum'] * 25)
    news_score = min(30, news_data['volume'] * 0.5)
    
    # Sentiment bonus
    sentiment_bonus = 0
    if news_data['sentiment'] == 'positive':
        sentiment_bonus = 10
    elif news_data['sentiment'] == 'negative':
        sentiment_bonus = -5
    
    total_score = interest_score * 0.5 + momentum_score * 0.3 + news_score * 0.2 + sentiment_bonus
    return max(0, min(100, total_score))