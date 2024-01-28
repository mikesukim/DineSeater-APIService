import json

from source.constant_variables import TOPIC_ARN_PREFIX,STAGE,TEST_PHONE_NUMBERS

class WaitinglistSNSPublisher:
    def __init__(self, sns_client):
        self.sns_client = sns_client
    
    def publish_new_waiting(self, business_name, new_waiting):
        topic_arn = TOPIC_ARN_PREFIX + business_name
        print("sns is publishing new waiting: ", new_waiting)
        print(new_waiting)
        message = self.create_fcm_message("new customer is on line!", "New waiting is added.", new_waiting)
        # Publish the message to the SNS topic
        # TODO : add error handling, learn how how to handle fcm error at SNS level
        response = self.sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageStructure='json'
        )
        print("response from sns publish: ", response)
        return response['MessageId']
    
    def publish_waiting_status_update(self, business_name, updated_waiting, waiting_status):
        topic_arn = TOPIC_ARN_PREFIX + business_name
        print("sns is publishing waiting status update: ", waiting_status)
        print(updated_waiting)
        message = self.create_fcm_message("waiting status update!", "open the app for the latest update.", updated_waiting)
        
        # Publish the message to the SNS topic
        response = self.sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageStructure='json'
        )
        print("response from sns publish: ", response)
        return response['MessageId']
    
    def create_fcm_message(self, title, body, data):
        # There should be only one backslash at a time in the message. Having consecutive backslashes will not publish the message, without any error message.
        # TODO : notification is sent silent all the time (to fix receiving notification issue when app is on background). Need to figure out how to send notification with badge & sounds
        message = {
            "default": "Sample fallback message",
            "GCM": "{ \"notification\": { \"title\": \"" + title + "\", \"body\": \"" + body + "\"}, \"data\": { \"priority\": \"high\", \"waiting\" :" + json.dumps(data, ensure_ascii=False)  + "}}",
        }
        return json.dumps(message)
    
    def publish_sms(self, phone_number, message):
        # if stage is not prod, then check if phone number is in the whitelist. if not, then don't send sms
        if STAGE != "PROD":
            if phone_number not in TEST_PHONE_NUMBERS:
                print("SMS is not sent at TEST stage. only sent to allowlisted phone numbers")
                return "BYPASS_SMS_SENDING_AT_TEST_STAGE"

        response = self.sns_client.publish(
            PhoneNumber=phone_number,
            Message=message
        )
        print("response from SMS publish: ", response)
        return response['MessageId'] 