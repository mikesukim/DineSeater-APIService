import unittest
from unittest.mock import MagicMock

from tests import test_variables

from event_analyzer import get_business_name
from post_handler import PostHandler

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
        post_action_handler = PostHandler(event, business_name, dynamodb_client)

        expected_result = 'add'
        result = post_action_handler.get_action()
        self.assertEqual(result, expected_result)

    def test_nonexistent_action(self):
        event = test_variables.post_without_body_request_event
        business_name = 'gilson'
        dynamodb_client = MagicMock()
        post_action_handler = PostHandler(event, business_name, dynamodb_client)

        self.assertRaises(Exception, post_action_handler.get_action, event)

    def test_gilson_get_table_type_success(self):
        event = test_variables.post_add_request_event
        business_name = 'gilson'
        dynamodb_client = MagicMock()
        post_action_handler = PostHandler(event, business_name, dynamodb_client)        
        detail_attribute = post_action_handler.get_detail_attribute()
        
        expected_result = (True, True)
        result = post_action_handler.get_table_type(detail_attribute)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
