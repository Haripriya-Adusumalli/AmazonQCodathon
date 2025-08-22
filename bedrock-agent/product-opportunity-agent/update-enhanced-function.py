import boto3
import zipfile

def update_enhanced_function():
    """Update enhanced-market-demand-copy with real API integration"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    with zipfile.ZipFile("enhanced-market-demand-real.zip", 'w') as zip_file:
        zip_file.write("lambda/enhanced-market-demand-real-api.py", "lambda_function.py")
    
    with open("enhanced-market-demand-real.zip", 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='enhanced-market-demand-copy',
            ZipFile=zip_file.read()
        )
    
    # Add environment variables for API keys
    lambda_client.update_function_configuration(
        FunctionName='enhanced-market-demand-copy',
        Environment={
            'Variables': {
                'NEWS_API_KEY': 'your_news_api_key_here',
                'GOOGLE_TRENDS_API_KEY': 'your_google_api_key_here'
            }
        },
        Timeout=30
    )
    
    print("Updated enhanced-market-demand-copy with real API integration")
    print("Note: Add your actual API keys to environment variables for real API calls")

if __name__ == "__main__":
    update_enhanced_function()