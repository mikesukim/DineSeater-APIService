import json
from source import response_handler
from source.waiting_status import WaitingStatus

class PostHandler:
    def __init__(self, event, business_name, dynamodb_client, waitinglist_sns_publisher):
        self.event = event
        self.business_name = business_name
        self.dynamodb_client = dynamodb_client
        self.waitinglist_sns_publisher = waitinglist_sns_publisher

    def handle_action(self):
        try:
            action = self.get_action()
            if action == 'add':
                return self.handle_add_action()
            elif action == 'remove':
                return self.handle_remove_action()
            elif action == 'notify':
                return self.handle_notify_action()
            elif action == 'report_arrival':
                return self.handle_report_arrival_action()
            elif action == 'report_missed':
                return self.handle_report_missed_action()
            else:
                return response_handler.failure({"message": "Action not allowed"})
        except Exception as e:
            error_message = 'Error handling action: ' + str(e)
            print(error_message)
            return response_handler.bad_request({"message": error_message})
    
    def get_action(self):
        body = json.loads(self.event['body'])
        action = body.get('action')
        if action is None:
            raise Exception('Action not found')
        return action.lower()

    def handle_add_action(self):
        number_of_customers = self.get_number_of_customers()
        detail_attribute = self.get_detail_attribute()
        phone_number = self.get_phone_number()

        if self.business_name == 'gilson':
            table_type = self.get_table_type(detail_attribute)

        # Create new waiting
        new_waiting = self.dynamodb_client.create_waiting(
            self.business_name,
            number_of_customers,
            detail_attribute,
            phone_number
        )
        print("Created new waiting: " + json.dumps(new_waiting))

        self.waitinglist_sns_publisher.publish_new_waiting(self.business_name, new_waiting)

        response_body = {
            "message": "Successfully added new waiting",
            "waiting": new_waiting
        }

        return response_handler.success(response_body)

    def handle_remove_action(self):
        waiting_id = self.get_waiting_id()

        # delete waiting
        self.dynamodb_client.delete_waiting(self.business_name, waiting_id)
        return response_handler.success({"message": "waiting deletion success " + waiting_id})

    def handle_notify_action(self):
        self.dynamodb_client.update_waiting_status(self.business_name, self.get_waiting_id(), WaitingStatus.TEXT_SENT.value)
        self.waitinglist_sns_publisher.publish_waiting_status_update(self.business_name, self.get_waiting_id(), WaitingStatus.TEXT_SENT.value)
        return response_handler.success({"message": "Notify action completed"})
    
    def handle_report_arrival_action(self):
        self.dynamodb_client.update_waiting_status(self.business_name, self.get_waiting_id(), WaitingStatus.ARRIVED.value)
        self.waitinglist_sns_publisher.publish_waiting_status_update(self.business_name, self.get_waiting_id(), WaitingStatus.ARRIVED.value)
        return response_handler.success({"message": "Report_arrival action completed"})
    
    def handle_report_missed_action(self):
        self.dynamodb_client.update_waiting_status(self.business_name, self.get_waiting_id(), WaitingStatus.MISSED.value)
        self.waitinglist_sns_publisher.publish_waiting_status_update(self.business_name, self.get_waiting_id(), WaitingStatus.MISSED.value)
        return response_handler.success({"message": "Report_missed action completed"})

    def get_number_of_customers(self):
        body = json.loads(self.event['body'])
        number_of_customers = body.get('number_of_customers')
        if number_of_customers is None:
            raise Exception('number_of_customers not found')
        return number_of_customers

    def get_detail_attribute(self):
        body = json.loads(self.event['body'])
        detail_attribute = body.get('detail_attribute')
        if detail_attribute is None:
            raise Exception('detail_attribute not found')
        return detail_attribute

    def get_table_type(self, detail_attribute):
        is_meal = detail_attribute.get('is_meal')
        is_grill = detail_attribute.get('is_grill')
        if is_meal is None or is_grill is None:
            raise Exception('table_type not found')
        return (is_meal, is_grill)

    def get_phone_number(self):
        body = json.loads(self.event['body'])
        phone_number = body.get('phone_number')
        if phone_number is None:
            raise Exception('phone_number not found')
        return phone_number

    def get_waiting_id(self):
        body = json.loads(self.event['body'])
        waiting_id = body.get('waiting_id')
        if waiting_id is None:
            raise Exception('waiting_id not found')
        return waiting_id
