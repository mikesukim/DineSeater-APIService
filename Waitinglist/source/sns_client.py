import json

class SNSClient:
    def __init__(self, sns_client):
        self.sns_client = sns_client
    
    def publish_message_to_sns(self):
        topic_arn = 'arn:aws:sns:us-west-2:112014237129:DineSeater-Test-Waitinglist-gilson'
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