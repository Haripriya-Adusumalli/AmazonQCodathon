import boto3
import json

def test_single_query():
    """Test a single query and check Lambda logs immediately after"""
    
    bedrock = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    logs_client = boto3.client('logs', region_name='us-east-1')
    
    agent_id = 'DKPL7RP9OU'
    alias_id = 'BIKYFE1L1K'
    
    query = "Analyze smart water bottle opportunity"
    
    print(f"Testing query: {query}")
    
    try:
        response = bedrock.invoke_agent(
            agentId=agent_id,
            agentAliasId=alias_id,
            sessionId="test-session-123",
            inputText=query
        )
        
        # Process response
        full_response = ""
        if response.get('completion'):
            for chunk in response['completion']:
                if chunk.get('chunk', {}).get('bytes'):
                    text = chunk['chunk']['bytes'].decode('utf-8')
                    full_response += text
        
        print(f"Response length: {len(full_response)}")
        print(f"Response: {full_response[:500]}...")
        
        # Check Lambda logs immediately
        import time
        time.sleep(5)  # Wait a bit for logs
        
        from datetime import datetime, timedelta
        start_time = int((datetime.now() - timedelta(minutes=2)).timestamp() * 1000)
        
        for func_name in ['market-demand-agent', 'competitor-scan-agent', 'capability-match-agent']:
            try:
                log_response = logs_client.filter_log_events(
                    logGroupName=f'/aws/lambda/{func_name}',
                    startTime=start_time
                )
                
                events = log_response.get('events', [])
                print(f"\n{func_name} - Recent invocations: {len(events)}")
                
            except Exception as e:
                print(f"\n{func_name} - Log error: {e}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_single_query()