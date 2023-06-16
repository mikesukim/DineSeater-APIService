import json
import os
from source import response_handler
from source import sns_client
from source import event_analyzer
import boto3

# Create an SNS client
sns = boto3.client('sns')
sns_client = sns_client.SNSClient(sns)

import json

def lambda_handler(event, context):
    
    # get business name from event (retrived from ID_TOKEN)
    business_name = None
    device_token = None

    print("Waitinglist API started with event: " + json.dumps(event))
    
    try:
        business_name = event_analyzer.get_business_name(event)
    except Exception as e:
        error_message = 'Error getting business name: ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "Business name not found"})
        
    try:
        device_token = event_analyzer.get_device_token(event)
        print("device_token: " + device_token)
    except Exception as e:
        error_message = 'Error getting device_token : ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "device_token name not found"})

    # TODO: move to env variable
    platform_application_arn = "arn:aws:sns:us-west-2:112014237129:app/GCM/DineSeater-Test-Flutter"

    is_device_registered = None
    try:
        is_device_registered = sns_client.check_device_token(device_token, platform_application_arn)
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
        endpoint_arn = sns_client.register_device_token(device_token, 
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
        topic_arn = sns_client.get_topic_arn(topic_name)
        print("get_topic_arn : " + str(topic_arn))
    except Exception as e:
        error_message = 'Error checking topic existence: ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "Error checking topic existence"})
    
    if topic_arn == None:
        topic_arn = sns_client.create_topic(topic_name)
        print("create_topic : " + str(topic_arn))
    
    # Subscribe the endpoint to the topic
    try:
        sns_client.subscribe_endpoint_to_topic(endpoint_arn, topic_arn)
    except Exception as e:
        error_message = 'Error subscribing endpoint to topic: ' + str(e)
        print(error_message)
        return response_handler.failure({"message": "Error subscribing endpoint to topic"})

    return response_handler.success({"message": "Device token is registered"})
