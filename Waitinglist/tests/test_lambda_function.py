import unittest
from tests import test_variables

from lambda_function import lambda_handler, get_claim

class TestLambdaFunction(unittest.TestCase):
    def test_nonexistent_claim(self):
        event = test_variables.post_request_event_without_business_name
        expected_status_code = 400
        
        result = lambda_handler(event, None)
        self.assertEqual(result['statusCode'], expected_status_code)
    
    def test_another_existing_claim(self):
        event = test_variables.post_add_request_event
        expected_status_code = 200
        
        result = lambda_handler(event, None)
        self.assertEqual(result['statusCode'], expected_status_code)
    
    def test_supported_http_request(self):
        event = test_variables.post_add_request_event
        expected_status_code = 200

        result = lambda_handler(event, None)
        self.assertEqual(result['statusCode'], expected_status_code)
    
    def test_not_supported_http_request(self):
        event = test_variables.put_request_event
        expected_status_code = 400
        
        result = lambda_handler(event, None)
        self.assertEqual(result['statusCode'], expected_status_code)

    def test_supported_action(self):
        event = test_variables.post_add_request_event
        expected_status_code = 200

        result = lambda_handler(event, None)
        self.assertEqual(result['statusCode'], expected_status_code)

    def test_nonexistent_action(self):
        event = test_variables.post_without_body_request_event
        expected_status_code = 400

        result = lambda_handler(event, None)
        self.assertEqual(result['statusCode'], expected_status_code)


if __name__ == '__main__':
    unittest.main()
