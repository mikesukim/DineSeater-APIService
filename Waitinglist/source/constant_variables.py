# env variables should only be at this file and whole project should use this file to access env variables
from dotenv import load_dotenv
import os

load_dotenv()

TOPIC_ARN_PREFIX = None
TABLE_NAME_WAITINGLIST = None
STAGE = None
TEST_PHONE_NUMBERS = None

match os.getenv('STAGE').upper():
    case 'TEST':
        TOPIC_ARN_PREFIX = os.getenv('TEST_TOPIC_ARN_PREFIX')
        TABLE_NAME_WAITINGLIST = os.getenv('TEST_DYNAMODB_TABLE_NAME_WAITINGLIST')
        STAGE = 'TEST'
        TEST_PHONE_NUMBERS=os.getenv('TEST_PHONE_NUMBER_ALLOWLIST').split(',')
    case 'PROD':
        TOPIC_ARN_PREFIX = os.getenv('PROD_TOPIC_ARN_PREFIX')
        TABLE_NAME_WAITINGLIST = os.getenv('PROD_DYNAMODB_TABLE_NAME_WAITINGLIST')
        STAGE = 'PROD'
    case _:
        print("STAGE not set")
        raise Exception("STAGE not set")
    
SMS_MESSAGE_WAITING_CREATION = "Welcome to the Gilson! You're all set on our waiting list! Just a heads up, when your table is ready, we kindly ask that you join us within 5 minutes, otherwise it will move to the next team. Thanks a bunch for choosing us!"
SMS_MESSAGE_TABLE_READY = "Hello! Your table is ready at the Gilson! Please come to the host stand within 5 minutes to be seated. We're excited to have you join us!"
PUSH_NOTIFICATION_TITLE = "Waiting List Update!"
PUSH_NOTIFICATION_BODY = "Your update is ready! Tap to see what's new."