import json
import decimal

from source import response_handler

class GetHandler:
    def __init__(self, event, business_name, dynamodb_client):
        self.event = event
        self.business_name = business_name
        self.dynamodb_client = dynamodb_client

    def handle_action(self):
        try:
            # get waitinglist from dynamodb
            # TODO: make sure the limited number of watitinglist (1MB) that can be retrieved at once.
            waitings = self.dynamodb_client.get_today_waitings_by_business_name(self.business_name)
            print('Successfully get waitings: ' + str(waitings))
            response_body = {
                "message": "Successfully get waitinglists",
                "waitings": waitings
            }
            # dynamodb returns number_of_customers as a Decimal type which is not JSON serializable. Convert it to int.
            def decimal_default(obj):
                if isinstance(obj, decimal.Decimal):
                    return int(obj)
                raise TypeError
            
            return response_handler.success(json.dumps(response_body, default=decimal_default))
        except Exception as e:
            error_message = 'Error while handling get request: ' + str(e)
            print(error_message)
            return response_handler.bad_request({"message": error_message})