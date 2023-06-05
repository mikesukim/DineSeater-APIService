import unittest
from tests import test_variables

from lambda_function import lambda_handler, get_claim, get_business_name, get_action

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
        expected_result = 'add'

        result = get_action(event)
        self.assertEqual(result, expected_result)

    def test_nonexistent_action(self):
        event = test_variables.post_without_body_request_event 
        self.assertRaises(Exception, get_action, event)


if __name__ == '__main__':
    unittest.main()
