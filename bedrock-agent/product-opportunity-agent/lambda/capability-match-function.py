import json

def lambda_handler(event, context):
    """Simple capability match function"""
    try:
        query = event.get('query', event.get('inputText', 'product'))
        
        result = {
            'capability_score': 70.0,
            'skill_matches': ['product_design', 'manufacturing'],
            'skill_gaps': ['specialized_expertise'],
            'supplier_readiness': 'Medium',
            'time_to_market': '6-12 months',
            'compliance_status': {'regulatory': 'Needs Review'},
            'recommended_actions': ['Conduct feasibility study']
        }
        
        return {'statusCode': 200, 'body': json.dumps(result)}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
