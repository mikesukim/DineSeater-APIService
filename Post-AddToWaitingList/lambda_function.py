import json

def lambda_handler(event, context):
    business_name = get_claim(event, 'business_name')  
    if not business_name or business_name == None:
        return {
            'statusCode': 400,
            'body': 'Business name not found'
        } 
    
    print("business name: " + business_name)
    return {
        'statusCode': 200,
        'body': 'Claim retrieved successfully'
    }


def get_claim(event, claim_name):
    authorizer = event['requestContext'].get('authorizer')
    if authorizer and 'claims' in authorizer:
        claims = authorizer['claims']
        if claim_name in claims:
            return claims[claim_name]
    return None
