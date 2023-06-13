import unittest
from unittest.mock import MagicMock

from tests import test_variables

from lambda_function import get_business_name

class TestLambdaFunction(unittest.TestCase):
    def test_existing_business_name(self):
        event = test_variables.post_add_request_event
        
        expected_business_name = 'gilson'
        result = get_business_name(event)
        self.assertEqual(result, expected_business_name)

    def test_nonexistent_business_name(self):
        event = test_variables.post_request_event_without_business_name
        
        self.assertRaises(Exception, get_business_name, event)

if __name__ == '__main__':
    unittest.main()
