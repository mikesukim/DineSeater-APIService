import json
import logging

import boto3

from source.cloudwatch_metrics_emitter import CloudWatchMetricsEmitter
from source import event_analyzer, response_handler, sns_client
from source.constant_variables import (PLATFORM_APPLICATION_ARN,
                                       TOPIC_NAME_PREFIX)

# Create an SNS client
sns = boto3.client('sns')
sns_client = sns_client.SNSClient(sns)

cloudwatch_metrics_emitter = CloudWatchMetricsEmitter()

import json

logger = logging.getLogger()

def lambda_handler(event, context):
    
    # get business name from event (retrived from ID_TOKEN)
    business_name = None
    device_token = None

    logger.info("Waitinglist API started with event: " + json.dumps(event))
    
    try:
        business_name = event_analyzer.get_business_name(event)
    except Exception as e:
        error_message = 'Error getting business name: ' + str(e)
        logger.error(error_message)
        cloudwatch_metrics_emitter.emit_metric("DeviceTokenRegistrationAPIError", 1, "Count")
        return response_handler.failure({"message": "Business name not found"})
        
    try:
        device_token = event_analyzer.get_device_token(event)
        logger.info("device_token: " + device_token)
    except Exception as e:
        error_message = 'Error getting device_token : ' + str(e)
        logger.error(error_message)
        cloudwatch_metrics_emitter.emit_metric("DeviceTokenRegistrationAPIError", 1, "Count")
        return response_handler.failure({"message": "device_token name not found"})

    platform_application_arn = PLATFORM_APPLICATION_ARN
    is_device_registered = None
    try:
        is_device_registered = sns_client.check_device_token(device_token, platform_application_arn)
        logger.info("check_device_token : " + str(is_device_registered))
    except Exception as e:
        error_message = 'Error checking device token: ' + str(e)
        logger.error(error_message)
        cloudwatch_metrics_emitter.emit_metric("DeviceTokenRegistrationAPIError", 1, "Count")
        return response_handler.failure({"message": "Error checking device token"})
    
    if is_device_registered:
        # If the device token is already registered to its application platform, then assume this endpoint is already subscribed to the topic. 
        return response_handler.success({"message": "Device token is already registered"})
    
    # Register device token to the application platform
    endpoint_arn = None
    try:
        endpoint_arn = sns_client.register_device_token(device_token, platform_application_arn)
    except Exception as e:
        error_message = 'Error registering device token: ' + str(e)
        logger.error(error_message)
        cloudwatch_metrics_emitter.emit_metric("DeviceTokenRegistrationAPIError", 1, "Count")
        return response_handler.failure({"message": "Error registering device token"})
    
    # Check if topic exists for its business.
    topic_arn = None
    topic_name = TOPIC_NAME_PREFIX + business_name

    try:
        topic_arn = sns_client.get_topic_arn(topic_name)
        logger.info("get_topic_arn : " + str(topic_arn))
    except Exception as e:
        error_message = 'Error checking topic existence: ' + str(e)
        logger.error(error_message)
        cloudwatch_metrics_emitter.emit_metric("DeviceTokenRegistrationAPIError", 1, "Count")
        return response_handler.failure({"message": "Error checking topic existence"})
    
    if topic_arn == None:
        topic_arn = sns_client.create_topic(topic_name)
        logger.info("create_topic : " + str(topic_arn))
    
    # Subscribe the endpoint to the topic
    try:
        sns_client.subscribe_endpoint_to_topic(endpoint_arn, topic_arn)
    except Exception as e:
        error_message = 'Error subscribing endpoint to topic: ' + str(e)
        logger.error(error_message)
        cloudwatch_metrics_emitter.emit_metric("DeviceTokenRegistrationAPIError", 1, "Count")
        return response_handler.failure({"message": "Error subscribing endpoint to topic"})

    return response_handler.success({"message": "Device token is registered"})
