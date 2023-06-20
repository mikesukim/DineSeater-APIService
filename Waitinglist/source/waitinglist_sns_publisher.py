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
        except Exception as e:
            print("Error publishing message:", str(e))
            return {
                'statusCode': 500,
                'body': 'Error publishing message'
            }
        return response['MessageId']
    
    def create_fcm_message(self, title, body, data):
        message = {
            "default": "Sample fallback message",
            "GCM": "{ \"notification\": { \"title\": \"" + title + "\", \"body\": \"" + body + "\"}, \"data\": " + json.dumps(data)  + "}",
        }
        return json.dumps(message)