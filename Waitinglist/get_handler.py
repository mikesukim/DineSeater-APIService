import json
import response_handler

class GetHandler:
    def __init__(self, event, business_name, dynamodb_client):
        self.event = event
        self.business_name = business_name
        self.dynamodb_client = dynamodb_client

    def handle_action(self):
        try:
            # get waitinglist from dynamodb
            return response_handler.success({"message": "Hello " + self.business_name})
        except Exception as e:
            error_message = 'Error handling get request: ' + str(e)
            print(error_message)
            return response_handler.bad_request({"message": error_message})