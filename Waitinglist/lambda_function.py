import json
import logging

import boto3
import source.response_handler as response_handler
from source.cloudwatch_metrics_emitter import CloudWatchMetricsEmitter
from source.constant_variables import TABLE_NAME_WAITINGLIST
from source.dynamodb_client import DynamoDBClient
from source.event_analyzer import get_business_name
from source.get_handler import GetHandler
from source.post_handler import PostHandler
from source.waitinglist_sns_publisher import WaitinglistSNSPublisher

# Global variable to make singleton within a container.
dynamodb_client = DynamoDBClient(TABLE_NAME_WAITINGLIST)
waitinglistSNSPublisher = WaitinglistSNSPublisher(boto3.client('sns'))
cloudwatch_metrics_emitter = CloudWatchMetricsEmitter()

logger = logging.getLogger()

def lambda_handler(event, context):
    # get business name from event (retrieve from ID_TOKEN)
    logger.info("Waitinglist API started with event: " + json.dumps(event))
    try:
        business_name = get_business_name(event)
        match event['httpMethod']:
            case 'GET':
                get_action_handler = GetHandler(event, business_name, dynamodb_client)
                return get_action_handler.handle_action()

            case 'POST':
                post_action_handler = PostHandler(event, business_name, dynamodb_client, waitinglistSNSPublisher)
                return post_action_handler.handle_action()

            case _:
                return response_handler.failure({"message": "Method not allowed"})

    except Exception as e:
        error_message = 'Error handling WaitingList API request : ' + str(e)
        logger.error(error_message)
        cloudwatch_metrics_emitter.emit_metric("WaitingListAPIError", 1, "Count")
        return response_handler.failure({"message": f"Error handling WaitingList API request: {error_message}"})
