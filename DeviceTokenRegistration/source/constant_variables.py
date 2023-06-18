# env variables should only be at this file and whole project should use this file to access env variables
from dotenv import load_dotenv
import os

load_dotenv()

PLATFORM_APPLICATION_ARN = None
TOPIC_NAME_PREFIX = None

match os.getenv('STAGE').upper():
    case 'TEST':
        PLATFORM_APPLICATION_ARN = os.getenv('TEST_PLATFORM_APPLICATION_ARN')
        TOPIC_NAME_PREFIX = os.getenv('TOPIC_NAME_PREFIX')
    case 'PROD':
        PLATFORM_APPLICATION_ARN = os.getenv('PROD_PLATFORM_APPLICATION_ARN')
        TOPIC_NAME_PREFIX = os.getenv('TOPIC_NAME_PREFIX')
    case _:
        print("STAGE not set")
        raise Exception("STAGE not set")
    
