import unittest
from lambda_function import (
    add_business_name_to_user_attributes,
    add_business_name_to_token_id,
    get_user_attributes,
    set_user_attributes,
    get_claims_override_details,
    set_claims_override_details
)

class TestLambdaFunction(unittest.TestCase):
    def setUp(self):
        # Set up the event object for testing
        self.event = {
        }

    def test_sample(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
