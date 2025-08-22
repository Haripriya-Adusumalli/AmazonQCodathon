import boto3
from datetime import datetime, timedelta

def check_lambda_error():
    """Check recent Lambda function errors"""
    
    logs = boto3.client('logs', region_name='us-east-1')
    
    # Check all three Lambda functions
    functions = [
        'market-demand-agent',
        'competitor-scan-agent', 
        'capability-match-agent'
    ]
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=1)
    
    for func_name in functions:
        log_group = f'/aws/lambda/{func_name}'
        
        try:
            print(f"\\n=== {func_name} LOGS ===")
            
            response = logs.filter_log_events(
                logGroupName=log_group,
                startTime=int(start_time.timestamp() * 1000),
                endTime=int(end_time.timestamp() * 1000),
                filterPattern='ERROR'
            )
            
            if response['events']:
                for event in response['events'][-5:]:  # Last 5 errors
                    print(f"Time: {datetime.fromtimestamp(event['timestamp']/1000)}")
                    print(f"Message: {event['message']}")
                    print("---")
            else:
                print("No recent errors found")
                
        except Exception as e:
            print(f"Error checking {func_name}: {e}")

if __name__ == "__main__":
    check_lambda_error()