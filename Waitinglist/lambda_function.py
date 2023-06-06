import json
import response_handler
from dynamodb_client import DynamoDBClient

# Global variable to make singleton within a container.
dynamodb_client = DynamoDBClient('DineSeater-Waitinglist')

def lambda_handler(event, context):
    # get business name from event (retrived from ID_TOKEN)
    business_name = None
    print("Waitinglist API started with event: " + json.dumps(event))
    try:
        business_name = get_business_name(event)
    except Exception as e:
        print(e)
        return response_handler.failure({"message": "Business name not found"})
    
    # check http Method from event
    match event['httpMethod']:

        case 'GET':
            # get waitinglist from dynamodb
            return response_handler.success({"message": "Hello " + business_name})
        
        case 'POST':
            action = None
            try:
                action = get_action(event)
            except Exception as e:
                error_message = 'Error getting action: ' + str(e)
                print(error_message)
                return response_handler.bad_request({"message": "Action not found"})
            # TODO : create a abstract class for action
            match action :
                case 'add':
                    # add customer to waitinglist
                    # add waiting to dynamodb
                    print("Add customer to waitinglist")

                    # get attributes from body   
                    number_of_customers = None
                    detail_attribute = None
                    phone_number = None
                    try:
                        number_of_customers = get_number_of_customers(event)
                        detail_attribute =  get_detail_attribute(event)
                        phone_number = get_phone_number(event)
                        if business_name == 'gilson' :
                            get_table_type(detail_attribute)
                    except Exception as e:
                        error_message = 'Error getting attributes: ' + str(e)
                        print(error_message)
                        return response_handler.bad_request({"message": error_message})

                    # Create waiting
                    new_waiting = dynamodb_client.create_waiting(business_name, number_of_customers, detail_attribute, phone_number)
                    print("Created new waiting: " + json.dumps(new_waiting))
                
                    # TODO: publish sns message

                    return response_handler.success({"message": "waiting creation success " + new_waiting})

                case 'remove':
                    # remove customer from waitinglist
                    # remove waiting from dynamodb
                    print("Remove customer from waitinglist")
                    # get waiting_id from body
                    waiting_id = None
                    try:
                        waiting_id = get_waiting_id(event)
                    except Exception as e:
                        error_message = 'Error getting waiting_id: ' + str(e)
                        print(error_message)
                        return response_handler.bad_request({"message": error_message})
                    # delete waiting
                    dynamodb_client.delete_waiting(business_name, waiting_id)
                    return response_handler.success({"message": "waiting deletion success " + waiting_id})
                case 'notify':
                    # notify customer from waitinglist
                    # update dynamodb(waiting status) first, then perform sns publish
                    # publish sns message
                    print("Notify customer from waitinglist")
                case _:
                    print("Not supported action type : " + action)
                    return response_handler.failure({"message": "Action not allowed"})
            return response_handler.success({"message": "Hello " + business_name})
        
        case _:
            return response_handler.failure({"message": "Method not allowed"})


def get_business_name(event):
    business_name = get_claim(event, 'business_name')
    if business_name == None:
        raise Exception('Business name not found')
    return business_name.lower()

def get_claim(event, claim_name):
    authorizer = event['requestContext'].get('authorizer')
    if authorizer and 'claims' in authorizer:
        claims = authorizer['claims']
        if claim_name in claims:
            return claims[claim_name]
    return None

def get_action(event):
    body = json.loads(event['body'])
    action = body['action']
    if action == None:
        raise Exception('Action not found')
    return action.lower()

def get_number_of_customers(event):
    body = json.loads(event['body'])
    number_of_customers = body['number_of_customers']
    if number_of_customers == None:
        raise Exception('number_of_customers not found')
    return number_of_customers

def get_detail_attribute(event):
    body = json.loads(event['body'])
    detail_attribute = body['detail_attribute']
    if detail_attribute == None:
        raise Exception('detail_attribute not found')
    return detail_attribute

def get_table_type(detail_attribute):
    is_meal = detail_attribute['is_meal']
    is_grill = detail_attribute['is_grill']
    if is_meal == None or is_grill == None:
        raise Exception('table_type not found')
    return (is_meal, is_grill)

def get_phone_number(event):
    body = json.loads(event['body'])
    phone_number = body['phone_number']
    if phone_number == None:
        raise Exception('phone_number not found')
    return phone_number

def get_waiting_id(event):
    body = json.loads(event['body'])
    waiting_id = body['waiting_id']
    if waiting_id == None:
        raise Exception('waiting_id not found')
    return waiting_id
