import json
import response_handler

def lambda_handler(event, context):
    # get business name from event (retrived from ID_TOKEN)
    business_name = None
    print("Waitinglist API started with event: " + json.dumps(event))
    try:
        business_name = get_business_name(event)
    except Exception as e:
        print(e)
        return response_handler.failure({"message": "Business name not found"})
    
    # check http Method from event
    match event['httpMethod']:
        case 'GET':
            return response_handler.success({"message": "Hello " + business_name})
        case 'POST':
            return response_handler.success({"message": "Hello " + business_name})
        case _:
            return response_handler.failure({"message": "Method not allowed"})


def get_business_name(event):
    business_name = get_claim(event, 'business_name')
    if business_name == None:
        raise Exception('Business name not found')
    return business_name

def get_claim(event, claim_name):
    authorizer = event['requestContext'].get('authorizer')
    if authorizer and 'claims' in authorizer:
        claims = authorizer['claims']
        if claim_name in claims:
            return claims[claim_name]
    return None