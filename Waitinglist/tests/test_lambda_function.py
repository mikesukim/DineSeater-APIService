import unittest
import json
from unittest.mock import MagicMock

from tests import test_variables

from source.event_analyzer import get_business_name
from source.post_handler import PostHandler
from source.waitinglist_sns_publisher import WaitinglistSNSPublisher

class TestLambdaFunction(unittest.TestCase):
    def test_existing_business_name(self):
        event = test_variables.post_add_request_event
        
        expected_business_name = 'gilson'
        result = get_business_name(event)
        self.assertEqual(result, expected_business_name)

    def test_nonexistent_business_name(self):
        event = test_variables.post_request_event_without_business_name
        
        self.assertRaises(Exception, get_business_name, event)

    def test_supported_action(self):
        event = test_variables.post_add_request_event
        business_name = 'gilson'
        dynamodb_client = MagicMock()
        waitinglist_sns_publisher = MagicMock()
        post_action_handler = PostHandler(event, business_name, dynamodb_client, waitinglist_sns_publisher)

        expected_result = 'add'
        result = post_action_handler.get_action()
        self.assertEqual(result, expected_result)

    def test_nonexistent_action(self):
        event = test_variables.post_without_body_request_event
        business_name = 'gilson'
        dynamodb_client = MagicMock()
        waitinglist_sns_publisher = MagicMock()
        post_action_handler = PostHandler(event, business_name, dynamodb_client, waitinglist_sns_publisher)

        self.assertRaises(Exception, post_action_handler.get_action, event)

    def test_gilson_get_table_type_success(self):
        event = test_variables.post_add_request_event
        business_name = 'gilson'
        dynamodb_client = MagicMock()
        waitinglist_sns_publisher = MagicMock()
        post_action_handler = PostHandler(event, business_name, dynamodb_client, waitinglist_sns_publisher)        
        detail_attribute = post_action_handler.get_detail_attribute()
        
        expected_result = (True, True)
        result = post_action_handler.get_table_type(detail_attribute)
        self.assertEqual(result, expected_result)

    def test_waiting_sns_publisher_creating_fcm_message(self):
        event = test_variables.post_add_request_event
        business_name = 'gilson'
        dynamodb_client = MagicMock()
        waitinglist_sns_publisher = WaitinglistSNSPublisher(MagicMock())
        post_action_handler = PostHandler(event, business_name, dynamodb_client, waitinglist_sns_publisher) 
        
        title = 'new customer is on line!'
        body = 'New waiting is added.'
        data = {
            "business_name": "gilson",
            "waiting_id": "c8b52853-777a-4fc7-89b9-e2a814af31be",
            "date_created": "2023-06-19 06:52:13",
            "number_of_customers": 2,
            "detail_attribute": {
                "is_meal": False,
                "is_grill": True
            },
            "phone_number": "2222222222",
            "status": "waiting"
        }
        json_data = json.dumps(data)
        sns_message = waitinglist_sns_publisher.create_fcm_message(title, body, json_data)
        self.assertIsInstance(sns_message, str)


if __name__ == '__main__':
    unittest.main()
