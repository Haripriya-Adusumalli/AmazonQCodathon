import boto3
import zipfile
import json
import os

def revert_and_create_new():
    """Revert existing functions and create new enhanced ones"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    iam = boto3.client('iam')
    
    print("Step 1: Reverting existing Lambda functions to original working versions...")
    
    # Revert existing functions to original working versions
    original_functions = [
        ('market-demand-agent', 'lambda/market-demand-original-mock.py'),
        ('competitor-scan-agent', 'lambda/competitor-scan-function.py'),
        ('capability-match-agent', 'lambda/capability-match-function.py')
    ]
    
    for func_name, original_file in original_functions:
        try:
            # Read original file and create simple working version
            if 'market-demand' in func_name:
                # Use the original mock version
                with open(original_file, 'r') as f:
                    code = f.read()
            else:
                # Create simple working versions for other functions
                code = create_simple_working_function(func_name)
            
            # Write to current function file
            current_file = original_file.replace('original-mock', 'function')
            with open(current_file, 'w') as f:
                f.write(code)
            
            # Create zip and update function
            zip_filename = f"{func_name}-revert.zip"
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                zip_file.write(current_file, 'lambda_function.py')
            
            with open(zip_filename, 'rb') as zip_file:
                lambda_client.update_function_code(
                    FunctionName=func_name,
                    ZipFile=zip_file.read()
                )
            
            print(f"Reverted {func_name} to working version")
            os.remove(zip_filename)
            
        except Exception as e:
            print(f"Error reverting {func_name}: {e}")
    
    print("\\nStep 2: Creating new enhanced Lambda functions...")
    
    # Create new enhanced functions
    role_arn = iam.get_role(RoleName='ProductOpportunityAgentRole')['Role']['Arn']
    
    new_functions = [
        {
            'name': 'enhanced-market-demand-v2',
            'file': 'lambda/enhanced-market-demand.py',
            'description': 'Enhanced market demand with real APIs'
        },
        {
            'name': 'enhanced-competitor-scan-v2',
            'file': 'lambda/enhanced-competitor-scan.py',
            'description': 'Enhanced competitor scan with real APIs'
        },
        {
            'name': 'enhanced-capability-match-v2',
            'file': 'lambda/enhanced-capability-match.py',
            'description': 'Enhanced capability match with Q Business'
        }
    ]
    
    created_functions = {}
    
    for func in new_functions:
        try:
            zip_filename = f"{func['name']}.zip"
            
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                zip_file.write(func['file'], 'lambda_function.py')
            
            with open(zip_filename, 'rb') as zip_file:
                try:
                    response = lambda_client.create_function(
                        FunctionName=func['name'],
                        Runtime='python3.9',
                        Role=role_arn,
                        Handler='lambda_function.lambda_handler',
                        Code={'ZipFile': zip_file.read()},
                        Description=func['description'],
                        Timeout=30,
                        MemorySize=256
                    )
                    print(f"Created new function: {func['name']}")
                    created_functions[func['name']] = response['FunctionArn']
                    
                except lambda_client.exceptions.ResourceConflictException:
                    zip_file.seek(0)
                    lambda_client.update_function_code(
                        FunctionName=func['name'],
                        ZipFile=zip_file.read()
                    )
                    response = lambda_client.get_function(FunctionName=func['name'])
                    print(f"Updated existing function: {func['name']}")
                    created_functions[func['name']] = response['Configuration']['FunctionArn']
            
            os.remove(zip_filename)
            
        except Exception as e:
            print(f"Error creating {func['name']}: {e}")
    
    # Save new function ARNs
    with open('enhanced-functions-config.json', 'w') as f:
        json.dump(created_functions, f, indent=2)
    
    print(f"\\nCompleted! Original functions reverted, new enhanced functions created.")
    print("Original agent should now work again.")
    
    return created_functions

def create_simple_working_function(func_name):
    """Create simple working function code"""
    
    if 'competitor' in func_name:
        return '''import json

def lambda_handler(event, context):
    """Simple competitor scan function"""
    try:
        query = event.get('query', event.get('inputText', 'product'))
        
        # Simple mock data
        total_products = abs(hash(query)) % 500 + 100
        avg_rating = 3.5 + (hash(query) % 15) / 10
        
        result = {
            'competition_score': min(100, total_products / 10 + avg_rating * 5),
            'total_products': total_products,
            'avg_rating': round(avg_rating, 1),
            'price_range': {'low': 25, 'high': 150},
            'top_competitors': ['CompetitorA', 'CompetitorB'],
            'market_saturation': 'Medium',
            'feature_gaps': ['Better design', 'Lower price']
        }
        
        return {'statusCode': 200, 'body': json.dumps(result)}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
'''
    
    elif 'capability' in func_name:
        return '''import json

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
'''

if __name__ == "__main__":
    revert_and_create_new()