import json
import response_handler
from dynamodb_client import DynamoDBClient
from post_handler import PostHandler
from get_handler import GetHandler

# Global variable to make singleton within a container.
dynamodb_client = DynamoDBClient('DineSeater-Waitinglist')

def lambda_handler(event, context):
    # get business name from event (retrived from ID_TOKEN)
    business_name = None
    print("Waitinglist API started with event: " + json.dumps(event))
    try:
        business_name = get_business_name(event)
    except Exception as e:
        error_message = 'Error getting business name: ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "Business name not found"})
    
    # check http Method from event
    match event['httpMethod']:
        case 'GET':
            get_action_handler = GetHandler(event, business_name, dynamodb_client)
            return get_action_handler.handle_action()
        
        case 'POST':
            post_action_handler = PostHandler(event, business_name, dynamodb_client)
            return post_action_handler.handle_action()       
         
        case _:
            return response_handler.failure({"message": "Method not allowed"})


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