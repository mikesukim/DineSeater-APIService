import json

from source.constant_variables import TOPIC_ARN_PREFIX

class WaitinglistSNSPublisher:
    def __init__(self, sns_client):
        self.sns_client = sns_client
    
    def publish_new_waiting(self, business_name, new_waiting):
        topic_arn = TOPIC_ARN_PREFIX + business_name
        message = self.create_fcm_message("new customer is on line!", "New waiting is added.", new_waiting)
        try:
            # Publish the message to the SNS topic
            response = self.sns_client.publish(
                TopicArn=topic_arn,
                Message=message,
                MessageStructure='json'
            )
            print("response from sns publish: ", response)
        except Exception as e:
            print("Error publishing message:", str(e))
            return {
                'statusCode': 500,
                'body': 'Error publishing message'
            }
        return response['MessageId']
    
    def publish_waiting_status_update(self, business_name, waiting_id, waiting_status):
        topic_arn = TOPIC_ARN_PREFIX + business_name
        data = {"waiting_id": waiting_id, "waiting_status": waiting_status}
        message = self.create_fcm_message("waiting status update!", "open the app for the latest update.", data)
        try:
            # Publish the message to the SNS topic
            response = self.sns_client.publish(
                TopicArn=topic_arn,
                Message=message,
                MessageStructure='json'
            )
            print("response from sns publish: ", response)
        except Exception as e:
            print("Error publishing message:", str(e))
            return {
                'statusCode': 500,
                'body': 'Error publishing message'
            }
        return response['MessageId']
    
    def create_fcm_message(self, title, body, data):
        # There should be only one backslash at a time in the message. Having consecutive backslashes will not publish the message, without any error message.
        message = {
            "default": "Sample fallback message",
            "GCM": "{ \"notification\": { \"title\": \"" + title + "\", \"body\": \"" + body + "\"}, \"data\": " + json.dumps(data, ensure_ascii=False)  + "}",
        }
        return json.dumps(message)