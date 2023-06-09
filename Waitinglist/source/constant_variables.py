# env variables should only be at this file and whole project should use this file to access env variables
from dotenv import load_dotenv
import os

load_dotenv()

TOPIC_ARN_PREFIX = None
TABLE_NAME_WAITINGLIST = None

match os.getenv('STAGE').upper():
    case 'TEST':
        TOPIC_ARN_PREFIX = os.getenv('TEST_TOPIC_ARN_PREFIX')
        TABLE_NAME_WAITINGLIST = os.getenv('TEST_DYNAMODB_TABLE_NAME_WAITINGLIST')
    case 'PROD':
        TOPIC_ARN_PREFIX = os.getenv('PROD_TOPIC_ARN_PREFIX')
        TABLE_NAME_WAITINGLIST = os.getenv('PROD_DYNAMODB_TABLE_NAME_WAITINGLIST')
    case _:
        print("STAGE not set")
        raise Exception("STAGE not set")
    
