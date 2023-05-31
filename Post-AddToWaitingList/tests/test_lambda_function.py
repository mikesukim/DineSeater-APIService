import unittest

from lambda_function import get_claim

class TestLambdaFunction(unittest.TestCase):
    def setUp(self):
        # Set up the event object for testing
        self.event = {
            "body": "{\"some_key\": \"some_value\"}",
            "resource": "/your-resource",
            "path": "/your-path",
            "httpMethod": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "queryStringParameters": None,
            "pathParameters": None,
            "stageVariables": None,
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "sub": "your_user_id",
                        "email": "john@example.com",
                        "business_name": "Gilson"
                    }
                },
                "httpMethod": "POST",
                "identity": {
                "sourceIp": "your-source-ip"
                },
                "stage": "prod",
                "requestId": "your-request-id",
                "requestTimeEpoch": 1619470000000,
                "requestTime": "your-request-time",
                "path": "/your-path",
                "accountId": "your-account-id",
                "protocol": "HTTP/1.1"
            }
        }

    def test_nonexistent_claim(self):
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'sub': 'user123',
                        'email': 'test@example.com'
                    }
                }
            }
        }
        claim_name = 'nonexistent'
        expected_error_response = 400
        
        result = get_claim(event, claim_name)
        
        self.assertIsNone(result)
        self.assertEqual(expected_error_response, 400)
    
    def test_another_existing_claim(self):
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'sub': 'user123',
                        'email': 'test@example.com',
                        'business_name': 'Gilson'
                    }
                }
            }
        }
        claim_name = 'business_name'
        expected_claim_value = 'Gilson'
        
        result = get_claim(event, claim_name)
        
        self.assertEqual(result, expected_claim_value)

if __name__ == '__main__':
    unittest.main()
