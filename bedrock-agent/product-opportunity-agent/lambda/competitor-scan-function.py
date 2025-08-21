import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """Competitor Scan Agent - analyzes competition landscape"""
    
    try:
        query = event.get('query', '')
        category = event.get('category', 'general')
        
        # Mock Amazon/eBay API data (replace with actual APIs in production)
        competition_data = analyze_mock_competition(query)
        
        # Calculate competition score (lower = less competition = better)
        competition_score = calculate_competition_score(competition_data)
        
        result = {
            'competition_score': round(competition_score, 2),
            'total_products': competition_data['total_products'],
            'avg_rating': competition_data['avg_rating'],
            'price_range': competition_data['price_range'],
            'top_competitors': competition_data['top_competitors'],
            'market_saturation': competition_data['market_saturation'],
            'feature_gaps': competition_data['feature_gaps']
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

def analyze_mock_competition(query):
    """Mock competition analysis"""
    
    # Simulate varying competition levels based on query
    query_hash = hash(query)
    
    total_products = abs(query_hash) % 1000 + 50
    avg_rating = 3.5 + (query_hash % 15) / 10
    
    price_low = 10 + abs(query_hash) % 50
    price_high = price_low * (2 + abs(query_hash) % 3)
    
    competitors = [
        f"Brand{i}" for i in range(1, min(6, (abs(query_hash) % 5) + 2))
    ]
    
    # Market saturation based on product count
    if total_products > 500:
        saturation = "High"
    elif total_products > 200:
        saturation = "Medium"
    else:
        saturation = "Low"
    
    # Mock feature gaps
    gaps = [
        "Better battery life",
        "Improved design",
        "Lower price point",
        "Enhanced durability",
        "Smart features"
    ]
    
    return {
        'total_products': total_products,
        'avg_rating': round(avg_rating, 1),
        'price_range': {'low': price_low, 'high': price_high},
        'top_competitors': competitors,
        'market_saturation': saturation,
        'feature_gaps': gaps[:3]
    }

def calculate_competition_score(data):
    """Calculate competition score (0-100, lower is better)"""
    
    # Factors that increase competition score (bad for opportunity)
    product_density = min(50, data['total_products'] / 20)
    rating_factor = (data['avg_rating'] - 3.0) * 10  # Higher ratings = more competition
    
    saturation_map = {'Low': 10, 'Medium': 30, 'High': 50}
    saturation_score = saturation_map.get(data['market_saturation'], 30)
    
    competition_score = product_density + rating_factor + saturation_score
    
    return max(0, min(100, competition_score))