import json

from source.constant_variables import TOPIC_ARN_PREFIX

class WaitinglistSNSPublisher:
    def __init__(self, sns_client):
        self.sns_client = sns_client
    
    def publish_message_to_sns(self, business_name):
        topic_arn = TOPIC_ARN_PREFIX + business_name
        message = {
            "default": "Sample fallback message",
            "GCM": "{ \"notification\": { \"title\": \"This is title\", \"body\": \"this is body\" }, \"data\": { \"message\": \"Sample message for FCM endpoints\" } }",
        }
        message_json = json.dumps(message)
        try:
            # Publish the message to the SNS topic
            response = self.sns_client.publish(
                TopicArn=topic_arn,
                Message=message_json,
                MessageStructure='json'
            )
        except Exception as e:
            print("Error publishing message:", str(e))
            return {
                'statusCode': 500,
                'body': 'Error publishing message'
            }
        return response['MessageId']