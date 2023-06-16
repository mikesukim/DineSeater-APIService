class SNSClient:
    def __init__(self, sns_client):
        self.sns_client = sns_client
    
    def check_device_token(self, device_token, platform_application_arn):
        # List all the endpoints registered with the specified platform application ARN
        response = self.sns_client.list_endpoints_by_platform_application(
            PlatformApplicationArn=platform_application_arn
        )

        # Iterate over the endpoints and check if the device token matches
        for endpoint in response['Endpoints']:
            if endpoint['Attributes']['Token'] == device_token:
                return True
        
        # If the device token is not found among the endpoints, return False
        return False

    def register_device_token(self, device_token, platform_application_arn):
        # Create an endpoint with the device token
        response = self.sns_client.create_platform_endpoint(
            PlatformApplicationArn=platform_application_arn,
            Token=device_token
        )

        # Get the endpoint ARN, needed to subscribe to the endpoint
        endpoint_arn = response['EndpointArn']
        return endpoint_arn

    def get_topic_arn(self, topic_name):
        # List all the topics
        response = self.sns_client.list_topics()
        
        # Iterate over the topics and check if the specified topic name matches
        for topic in response['Topics']:
            if topic_name == topic['TopicArn'].split(':')[-1]:
                return topic['TopicArn']
        
        # If the specified topic name is not found among the topics, return None
        return None

    def create_topic(self, topic_name):
        # Create a topic with the specified topic name
        response = self.sns_client.create_topic(Name=topic_name)
        
        # Get the topic ARN, needed to subscribe to the topic
        topic_arn = response['TopicArn']
        return topic_arn

    def subscribe_endpoint_to_topic(self, endpoint_arn, topic_arn):
        # Subscribe to the specified topic
        response = self.sns_client.subscribe(
            Endpoint=endpoint_arn,
            Protocol='application',
            TopicArn=topic_arn
        )
        
        # Get the subscription ARN, needed to publish to the topic
        subscription_arn = response['SubscriptionArn']
        return subscription_arn
