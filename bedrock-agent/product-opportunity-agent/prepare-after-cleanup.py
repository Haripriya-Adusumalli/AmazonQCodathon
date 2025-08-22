import boto3
import time

def prepare_after_cleanup():
    """Prepare agent after manual cleanup"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = 'DKPL7RP9OU'
    
    print("Preparing agent after cleanup...")
    bedrock.prepare_agent(agentId=agent_id)
    
    print("Waiting for preparation...")
    time.sleep(30)
    
    print("Agent prepared successfully")

if __name__ == "__main__":
    prepare_after_cleanup()