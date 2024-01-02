import json

from source.constant_variables import TOPIC_ARN_PREFIX

class WaitinglistSNSPublisher:
    def __init__(self, sns_client):
        self.sns_client = sns_client
    
    def publish_new_waiting(self, business_name, new_waiting):
        topic_arn = TOPIC_ARN_PREFIX + business_name
        message = self.create_fcm_message("new customer is on line!", "New waiting is added.", new_waiting)
        
        # Publish the message to the SNS topic
        response = self.sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageStructure='json'
        )
        print("response from sns publish: ", response)
        return response['MessageId']
    
    def publish_waiting_status_update(self, business_name, waiting_id, waiting_status):
        topic_arn = TOPIC_ARN_PREFIX + business_name
        data = {"waiting_id": waiting_id, "waiting_status": waiting_status}
        message = self.create_fcm_message("waiting status update!", "open the app for the latest update.", data)
        
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
        message = {
            "default": "Sample fallback message",
            "GCM": "{ \"notification\": { \"title\": \"" + title + "\", \"body\": \"" + body + "\"}, \"data\": { \"waiting\" :" + json.dumps(data, ensure_ascii=False)  + "}}",
        }
        return json.dumps(message)
    
    def publish_sms(self, phone_number, message):
        response = self.sns_client.publish(
            PhoneNumber=phone_number,
            Message=message
        )
        print("response from SMS publish: ", response)
        return response['MessageId'] 