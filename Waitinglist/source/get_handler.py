from source import response_handler

class GetHandler:
    def __init__(self, event, business_name, dynamodb_client, cloudwatch_metrics_emitter):
        self.event = event
        self.business_name = business_name
        self.dynamodb_client = dynamodb_client
        self.cloudwatch_metrics_emitter = cloudwatch_metrics_emitter

    def handle_action(self):
        try:
            # get waitinglist from dynamodb
            # TODO: make sure the limited number of watitinglist (1MB) that can be retrieved at once.
            waitings = self.dynamodb_client.get_today_waitings_by_business_name(self.business_name)
            print('Successfully get waitings: ' + str(waitings))
            self.cloudwatch_metrics_emitter.emit_metric("WaitingListGetSuccess", 1, "Count")
            response_body = {
                "message": "Successfully get waitinglists",
                "waitings": waitings
            }        
            return response_handler.success(response_body)
        except Exception as e:
            error_message = 'Error while handling get request: ' + str(e)
            print(error_message)
            return response_handler.bad_request({"message": error_message})