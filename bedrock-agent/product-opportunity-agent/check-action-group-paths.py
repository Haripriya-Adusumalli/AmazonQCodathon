import boto3
import json

def check_action_group_paths():
    """Check action group API paths"""
    
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    enhanced_agent_id = 'BKWEM7GZQX'
    
    try:
        action_groups = bedrock.list_agent_action_groups(
            agentId=enhanced_agent_id,
            agentVersion='DRAFT'
        )
        
        for ag in action_groups['actionGroupSummaries']:
            details = bedrock.get_agent_action_group(
                agentId=enhanced_agent_id,
                agentVersion='DRAFT',
                actionGroupId=ag['actionGroupId']
            )
            
            print(f"Action Group: {ag['actionGroupName']}")
            
            # Check API schema
            if 'apiSchema' in details['agentActionGroup']:
                schema = details['agentActionGroup']['apiSchema']
                if 'payload' in schema:
                    schema_content = schema['payload']
                    print(f"Schema: {schema_content[:200]}...")
                    
                    # Try to parse as JSON to find API paths
                    try:
                        schema_json = json.loads(schema_content)
                        if 'paths' in schema_json:
                            for path, methods in schema_json['paths'].items():
                                print(f"  API Path: {path}")
                                for method, details in methods.items():
                                    print(f"    Method: {method}")
                    except:
                        print("  Could not parse schema as JSON")
            
            print()
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_action_group_paths()