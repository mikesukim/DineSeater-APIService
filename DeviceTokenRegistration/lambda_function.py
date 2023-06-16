import json
import firebase_admin
import os
from firebase_admin import auth, messaging, credentials
import response_handler
import boto3


# Path to the service account credentials JSON file
credentials_path = os.path.join(os.path.dirname(__file__), 'dineseater-gilsonapp-firebase-adminsdk-credentials.json')

# Initialize Firebase Admin SDK with the service account credentials
firebase_credentials = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(firebase_credentials)

# Create an SNS client
sns = boto3.client('sns')

import json

def lambda_handler(event, context):
    
    # get business name from event (retrived from ID_TOKEN)
    business_name = None
    device_token = None

    print("Waitinglist API started with event: " + json.dumps(event))
    
    try:
        business_name = get_business_name(event)
    except Exception as e:
        error_message = 'Error getting business name: ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "Business name not found"})
        
    try:
        device_token = get_device_token(event)
        print("device_token: " + device_token)
    except Exception as e:
        error_message = 'Error getting device_token : ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "device_token name not found"})

    # TODO: move to env variable
    platform_application_arn = "arn:aws:sns:us-west-2:112014237129:app/GCM/DineSeater-Test-Flutter"

    is_device_registered = None
    try:
        is_device_registered = check_device_token(device_token, platform_application_arn)
        print("check_device_token : " + str(is_device_registered))
    except Exception as e:
        error_message = 'Error checking device token: ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "Error checking device token"})
    
    if is_device_registered:
        # If the device token is already registered to its application platform, then assume this endpoint is already subscribed to the topic. 
        return response_handler.success({"message": "Device token is already registered"})
    
    # Register device token to the application platform
    endpoint_arn = None
    try:
        "TODO: move to env variable"
        endpoint_arn = register_device_token(device_token, 
                                             platform_application_arn)
    except Exception as e:
        error_message = 'Error registering device token: ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "Error registering device token"})
    
    # Check if topic exists for its business.
    topic_arn = None

    "TODO: move to env variable"
    stage = "Test"
    topic_name = "DineSeater-" + stage + "-" + "Waitinglist" + "-" + business_name

    try:
        topic_arn = get_topic_arn(topic_name)
        print("get_topic_arn : " + str(topic_arn))
    except Exception as e:
        error_message = 'Error checking topic existence: ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "Error checking topic existence"})
    
    if topic_arn == None:
        topic_arn = create_topic(topic_name)
        print("create_topic : " + str(topic_arn))
    
    # Subscribe the endpoint to the topic
    try:
        subscribe_endpoint_to_topic(endpoint_arn, topic_arn)
    except Exception as e:
        error_message = 'Error subscribing endpoint to topic: ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "Error subscribing endpoint to topic"})

    return response_handler.success({"message": "Device token is registered"})
        
        
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


def check_device_token(device_token, platform_application_arn):
    # List all the endpoints registered with the specified platform application ARN
    # TODO: if endpoints are more than 100, subsequent calls is required. Also larger endpoinds become expensive.
    # Find other effiecient way to check if the device token is registered.

    response = sns.list_endpoints_by_platform_application(
        PlatformApplicationArn=platform_application_arn
    )
    print("list_endpoints_by_platform_application response: " + str(response))
    # Iterate over the endpoints and check if the device token matches
    for endpoint in response['Endpoints']:
        if endpoint['Attributes']['Token'] == device_token:        
            return True
    
    # If the device token is not found among the endpoints, return False
    return False

def register_device_token(device_token, platform_application_arn):
    # Create an endpoint with the device token
    response = sns.create_platform_endpoint(
        PlatformApplicationArn=platform_application_arn,
        Token=device_token
    )
    print("create_platform_endpoint response: " + str(response))
    # Get the endpoint ARN, needed to subscribe to the endpoint
    endpoint_arn = response['EndpointArn']
    return endpoint_arn

def get_topic_arn(topic_name):
    # List all the topics
    # TODO: if topics are more than 100, subsequent calls is required. Also larger endpoinds become expensive.
    # Find other effiecient way to check if the topic exists. (this will be far future, since one business will have only one topic)
    response = sns.list_topics()
    
    # Iterate over the topics and check if the specified topic name matches
    for topic in response['Topics']:
        if topic_name == topic['TopicArn'].split(':')[-1]:
            return topic['TopicArn']
    
    # If the specified topic name is not found among the topics, return False
    return None

def create_topic(topic_name):
    # Create a topic with the specified topic name
    response = sns.create_topic(
        Name=topic_name
    )
    print("create_topic response: " + str(response))
    # Get the topic ARN, needed to subscribe to the topic
    topic_arn = response['TopicArn']
    return topic_arn

def subscribe_endpoint_to_topic(endpoint_arn, topic_arn):
    # Subscribe to the specified topic
    response = sns.subscribe(
        Endpoint=endpoint_arn,
        Protocol='application',
        TopicArn=topic_arn
    )
    print("subscribe response: " + str(response))
    # Get the subscription ARN, needed to publish to the topic
    subscription_arn = response['SubscriptionArn']
    return subscription_arn