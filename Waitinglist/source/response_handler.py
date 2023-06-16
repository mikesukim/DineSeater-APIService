# Create a object that handles the response to the client
import json
from http import HTTPStatus

def response(status_code: int, body: dict) -> dict:
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }

def success(body: dict) -> dict:
    return response(HTTPStatus.OK, body)

def failure(body: dict) -> dict:
    return response(HTTPStatus.BAD_REQUEST, body)

def unauthorized(body: dict) -> dict:
    return response(HTTPStatus.UNAUTHORIZED, body)

def forbidden(body: dict) -> dict:
    return response(HTTPStatus.FORBIDDEN, body)

def not_found(body: dict) -> dict:
    return response(HTTPStatus.NOT_FOUND, body)

def internal_server_error(body: dict) -> dict:
    return response(HTTPStatus.INTERNAL_SERVER_ERROR, body)

def bad_gateway(body: dict) -> dict:
    return response(HTTPStatus.BAD_GATEWAY, body)

def service_unavailable(body: dict) -> dict:
    return response(HTTPStatus.SERVICE_UNAVAILABLE, body)

def gateway_timeout(body: dict) -> dict:
    return response(HTTPStatus.GATEWAY_TIMEOUT, body)

def bad_request(body: dict) -> dict:
    return response(HTTPStatus.BAD_REQUEST, body)
