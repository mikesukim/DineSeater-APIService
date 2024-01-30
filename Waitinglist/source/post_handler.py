import json
from source.constant_variables import SMS_MESSAGE_TABLE_READY, SMS_MESSAGE_WAITING_CREATION
from source import response_handler
from source.waiting_status import WaitingStatus

class PostHandler:
    def __init__(self, event, business_name, dynamodb_client, waitinglist_sns_publisher, cloudwatch_metrics_emitter):
        self.event = event
        self.business_name = business_name
        self.dynamodb_client = dynamodb_client
        self.waitinglist_sns_publisher = waitinglist_sns_publisher
        self.cloudwatch_metrics_emitter = cloudwatch_metrics_emitter

    def handle_action(self):
        try:
            action = self._get_action()
            if action == 'add':
                return self.handle_add_action()
            elif action == 'publish': # For pushing notification
                return self.handle_publish_action()
            elif action == 'remove':
                return self.handle_remove_action()
            elif action == 'notify': # For pushing SMS
                return self.handle_notify_action()
            elif action == 'report_arrival':
                return self.handle_report_arrival_action()
            elif action == 'report_missed':
                return self.handle_report_missed_action()
            elif action == 'report_cancelled':
                return self.handle_report_cancelled_action()
            elif action == 'report_back_initial_status':
                return self.handle_report_back_initial_status_action()
            else:
                return response_handler.failure({"message": "Action not allowed"})
        except Exception as e:
            error_message = 'Error handling action: ' + str(e)
            print(error_message)
            return response_handler.internal_server_error({"message": error_message})
    
    def _get_action(self):
        body = json.loads(self.event['body'])
        action = body.get('action')
        if action is None:
            raise Exception('Action not found')
        return action.lower()

    def handle_add_action(self):
        # create new waiting at db
        number_of_customers = self.get_number_of_customers()
        name = self.get_name()
        detail_attribute = self.get_detail_attribute()
        phone_number = self.get_phone_number()
        if self.business_name == 'gilson':
            table_type = self.get_table_type(detail_attribute)
        new_waiting = self.dynamodb_client.create_waiting(
            self.business_name,
            name,
            number_of_customers,
            detail_attribute,
            phone_number
        )
        print("Created new waiting: " + json.dumps(new_waiting))

        # send SMS
        print("SNS is about to publish SMS")
        # TODO : add customer name on text
        text_result = self.waitinglist_sns_publisher.publish_sms(phone_number, SMS_MESSAGE_WAITING_CREATION)
        print("SNS SMS result: " + text_result)

        response_body = {
            "message": "Successfully added new waiting",
            "waiting": new_waiting
        }
        self.cloudwatch_metrics_emitter.emit_metric("WaitingAddSuccess", 1, "Count")
        return response_handler.success(response_body)

    def handle_publish_action(self):
        # send push notification
        print("SNS is about to publish push notification")

        # get waiting from body
        body = json.loads(self.event['body'])
        waiting = body.get('waiting')
        if waiting is None:
            raise Exception('waiting not found')

        # publish push notification
        print("SNS is about to publish notification")
        notification_result = self.waitinglist_sns_publisher.publish_waiting(self.business_name, waiting)
        print("SNS notification result: " + notification_result)

        response_body = {
            "message": "Successfully pushed notification"
        }
        self.cloudwatch_metrics_emitter.emit_metric("WaitingPublishSuccess", 1, "Count")
        return response_handler.success(response_body)


    def handle_remove_action(self):
        waiting_id = self.get_waiting_id()

        # delete waiting
        self.dynamodb_client.delete_waiting(self.business_name, waiting_id)
        self.cloudwatch_metrics_emitter.emit_metric("WaitingRemoveSuccess", 1, "Count")
        return response_handler.success({"message": "waiting deletion success " + waiting_id})

    def handle_notify_action(self):
        # send SMS first this time
        phone_number_from_db = self.dynamodb_client.get_waiting_by_id(self.business_name, self.get_waiting_id()).get(
            'phone_number')
        print("SNS is about to publish SMS: " + phone_number_from_db)
        # TODO : phone number format check. raise error if sms is not available.
        text_reult = self.waitinglist_sns_publisher.publish_sms(phone_number_from_db, SMS_MESSAGE_TABLE_READY)
        print("SNS SMS result: " + text_reult)

        # update waiting status at db
        new_waiting = self.dynamodb_client.update_waiting_status(self.business_name, self.get_waiting_id(), WaitingStatus.TEXT_SENT.value)

        response_body = {
            "message": "Successfully updated waiting",
            "waiting": new_waiting
        }
        self.cloudwatch_metrics_emitter.emit_metric("WaitingNotifySuccess", 1, "Count")
        return response_handler.success(response_body)
    
    def handle_report_arrival_action(self):
        new_waiting = self.dynamodb_client.update_waiting_status(self.business_name, self.get_waiting_id(), WaitingStatus.ARRIVED.value)
        response_body = {
            "message": "Successfully updated waiting",
            "waiting": new_waiting
        }
        self.cloudwatch_metrics_emitter.emit_metric("WaitingReportArrivalSuccess", 1, "Count")
        return response_handler.success(response_body)
    
    def handle_report_missed_action(self):
        new_waiting = self.dynamodb_client.update_waiting_status(self.business_name, self.get_waiting_id(), WaitingStatus.MISSED.value)
        response_body = {
            "message": "Successfully updated waiting",
            "waiting": new_waiting
        }
        self.cloudwatch_metrics_emitter.emit_metric("WaitingReportMissedSuccess", 1, "Count")
        return response_handler.success(response_body)

    def handle_report_cancelled_action(self):
        new_waiting = self.dynamodb_client.update_waiting_status(self.business_name, self.get_waiting_id(), WaitingStatus.CANCELLED.value)
        response_body = {
            "message": "Successfully updated waiting",
            "waiting": new_waiting
        }
        self.cloudwatch_metrics_emitter.emit_metric("WaitingReportCancelledSuccess", 1, "Count")
        return response_handler.success(response_body)

    def handle_report_back_initial_status_action(self):
        new_waiting = self.dynamodb_client.update_waiting_status(self.business_name, self.get_waiting_id(), WaitingStatus.WAITING.value)
        response_body = {
            "message": "Successfully updated waiting",
            "waiting": new_waiting
        }
        self.cloudwatch_metrics_emitter.emit_metric("WaitingReportBackInitialStatusSuccess", 1, "Count")
        return response_handler.success(response_body)

    def get_number_of_customers(self):
        body = json.loads(self.event['body'])
        number_of_customers = body.get('number_of_customers')
        if number_of_customers is None:
            raise Exception('number_of_customers not found')
        return number_of_customers

    def get_name(self):
        body = json.loads(self.event['body'])
        name = body.get('name')
        if name is None:
            raise Exception('name not found')
        return name

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
