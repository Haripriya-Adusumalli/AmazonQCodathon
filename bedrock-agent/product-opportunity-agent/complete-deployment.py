import boto3
import json
import time

def complete_agent_deployment():
    """Complete the deployment of the product opportunity agent"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = 'DKPL7RP9OU'
    
    print(f"Completing deployment for agent: {agent_id}")
    
    # Wait for agent to be ready
    print("Waiting for agent to be ready...")
    for i in range(10):
        try:
            response = bedrock.get_agent(agentId=agent_id)
            status = response['agent']['agentStatus']
            print(f"Agent status: {status}")
            
            if status == 'NOT_PREPARED':
                break
            elif status == 'CREATING':
                time.sleep(30)
            else:
                break
        except Exception as e:
            print(f"Error checking status: {e}")
            time.sleep(30)
    
    # Prepare agent
    try:
        print("Preparing agent...")
        bedrock.prepare_agent(agentId=agent_id)
        time.sleep(45)
        
        # Create alias
        try:
            alias_response = bedrock.create_agent_alias(
                agentId=agent_id,
                agentAliasName='live',
                description='Live product opportunity analyzer'
            )
            alias_id = alias_response['agentAlias']['agentAliasId']
            print(f"Created alias: {alias_id}")
            
        except Exception as e:
            print(f"Alias creation failed: {e}")
            # Try to get existing alias
            try:
                aliases = bedrock.list_agent_aliases(agentId=agent_id)
                if aliases['agentAliasSummaries']:
                    alias_id = aliases['agentAliasSummaries'][0]['agentAliasId']
                    print(f"Using existing alias: {alias_id}")
                else:
                    alias_id = 'TSTALIASID'
                    print("Using test alias")
            except:
                alias_id = 'TSTALIASID'
                print("Using test alias")
        
        # Save configuration
        config = {
            'agentId': agent_id,
            'aliasId': alias_id,
            'region': 'us-east-1'
        }
        
        with open('product-opportunity-config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\nProduct Opportunity Agent deployed successfully!")
        print(f"Agent ID: {agent_id}")
        print(f"Alias ID: {alias_id}")
        print("\nUpdate your React app's aws-config.js with these values:")
        print(f"agentId: '{agent_id}'")
        print(f"aliasId: '{alias_id}'")
        
        return config
        
    except Exception as e:
        print(f"Error completing deployment: {e}")
        return None

if __name__ == "__main__":
    complete_agent_deployment()