'''
Entry point of lambda function's execution.
This lambda function will be executed at pre-token-generation phase as Cognito trigger.
'''

import json

def lambda_handler(event, context):
    return event