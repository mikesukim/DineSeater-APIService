post_request_event = {
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

post_add_request_event = {
    "body": "{\"action\": \"add\"}",
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

post_remove_request_event = {
    "body": "{\"action\": \"remove\"}",
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

post_notify_request_event = {
    "body": "{\"action\": \"notify\"}",
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

post_without_body_request_event = {
    "body": "{\"key\": \"value\"}",
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

post_request_event_without_business_name = {
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

get_request_event = {
    "resource": "/your-resource",
    "path": "/your-path",
    "httpMethod": "GET",
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
        "httpMethod": "GET",
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

put_request_event = {
    "body": "{\"some_key\": \"some_value\"}",
    "resource": "/your-resource",
    "path": "/your-path",
    "httpMethod": "PUT",
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
        "httpMethod": "PUT",
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