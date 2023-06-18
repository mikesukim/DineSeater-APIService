import json

import boto3
import source.response_handler as response_handler
from source import sns_client
from source.constant_variables import TABLE_NAME_WAITINGLIST
from source.dynamodb_client import DynamoDBClient
from source.event_analyzer import get_business_name
from source.get_handler import GetHandler
from source.post_handler import PostHandler

# Global variable to make singleton within a container.
dynamodb_client = DynamoDBClient(TABLE_NAME_WAITINGLIST)
sns = boto3.client('sns')

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
            post_action_handler = PostHandler(event, business_name, dynamodb_client, sns_client.SNSClient(sns))
            return post_action_handler.handle_action()       
         
        case _:
            return response_handler.failure({"message": "Method not allowed"})
