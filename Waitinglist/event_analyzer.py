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