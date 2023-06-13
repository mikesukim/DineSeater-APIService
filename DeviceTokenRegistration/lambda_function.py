import json
import firebase_admin
import os
from firebase_admin import auth, messaging, credentials
import response_handler


# Path to the service account credentials JSON file
credentials_path = os.path.join(os.path.dirname(__file__), 'dineseater-gilsonapp-firebase-adminsdk-credentials.json')

# Initialize Firebase Admin SDK with the service account credentials
firebase_credentials = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(firebase_credentials)


import json

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
        
    try:
        get_device_token = get_device_token(event)
    except Exception as e:
        error_message = 'Error getting device_token : ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "device_token name not found"})
        
    # TODO : subscribe device_token to topic (business_name) 
    return response_handler.success({"message": "device_token name found"})
        
        
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
    
def get_device_token(self):
    body = json.loads(self.event['body'])
    device_token = body.get('device_token')
    if device_token is None:
        raise Exception('device_token not found')
    return device_token