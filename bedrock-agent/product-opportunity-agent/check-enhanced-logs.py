import boto3
from datetime import datetime, timedelta

def check_enhanced_logs():
    """Check enhanced Lambda function logs"""
    
    logs_client = boto3.client('logs', region_name='us-east-1')
    
    func_name = 'enhanced-market-demand-copy'
    log_group = f'/aws/lambda/{func_name}'
    
    # Check logs from last 10 minutes
    start_time = int((datetime.now() - timedelta(minutes=10)).timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    
    try:
        response = logs_client.filter_log_events(
            logGroupName=log_group,
            startTime=start_time,
            endTime=end_time
        )
        
        events = response.get('events', [])
        print(f"Recent log events for {func_name}: {len(events)}")
        
        for event in events[-10:]:  # Show last 10 events
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
            print(f"{timestamp}: {event['message'].strip()}")
            
    except Exception as e:
        print(f"Error checking logs: {e}")

if __name__ == "__main__":
    check_enhanced_logs()