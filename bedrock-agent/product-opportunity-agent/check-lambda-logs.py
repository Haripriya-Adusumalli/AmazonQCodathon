import boto3
from datetime import datetime, timedelta

def check_lambda_logs():
    """Check recent Lambda function logs"""
    
    logs_client = boto3.client('logs', region_name='us-east-1')
    
    lambda_functions = ['market-demand-agent', 'competitor-scan-agent', 'capability-match-agent']
    
    # Check logs from last 10 minutes
    start_time = int((datetime.now() - timedelta(minutes=10)).timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    
    for func_name in lambda_functions:
        log_group = f'/aws/lambda/{func_name}'
        
        try:
            # Get recent log events
            response = logs_client.filter_log_events(
                logGroupName=log_group,
                startTime=start_time,
                endTime=end_time
            )
            
            events = response.get('events', [])
            print(f"\n{func_name} - Recent log events: {len(events)}")
            
            for event in events[-3:]:  # Show last 3 events
                timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
                print(f"  {timestamp}: {event['message'].strip()}")
                
        except Exception as e:
            print(f"\n{func_name} - Error checking logs: {e}")

if __name__ == "__main__":
    check_lambda_logs()