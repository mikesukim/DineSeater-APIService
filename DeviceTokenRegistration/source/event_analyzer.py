import json

def get_business_name(event):
    business_name = get_claim(event, 'business_name')
    if business_name == None:
        raise Exception('Business name not found')
    return business_name.lower()

def get_claim(event, claim_name):
    authorizer = event['requestContext'].get('authorizer')
    if authorizer and 'claims' in authorizer:
        claims = authorizer['claims']
        if claim_name in claims:
            return claims[claim_name]
    return None

def get_device_token(event):
    body = json.loads(event['body'])
    device_token = body.get('device_token')
    if device_token is None:
        raise Exception('device_token not found')
    return device_token
