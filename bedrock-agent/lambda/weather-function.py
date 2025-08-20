import json
import requests
import os

def lambda_handler(event, context):
    # Extract city from the agent's input
    city = event.get('inputText', '').strip()
    
    if not city:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'City name is required'})
        }
    
    # OpenWeatherMap API (you'll need to set API_KEY environment variable)
    api_key = os.environ.get('WEATHER_API_KEY')
    if not api_key:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Weather API key not configured'})
        }
    
    try:
        # Get current weather
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
            
            return {
                'statusCode': 200,
                'body': json.dumps(weather_info)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': f'Weather data not found for {city}'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }