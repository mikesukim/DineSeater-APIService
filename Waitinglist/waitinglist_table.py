import boto3
import uuid

class WaitingTable:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    def get_waiting_by_id(self, business_name, waiting_id):
        response = self.table.get_item(Key={'business_name': business_name, 'waiting_id': waiting_id})
        return response.get('Item')
    
    def get_waitings_by_business_name(self, business_name):
        response = self.table.query(
            KeyConditionExpression='business_name = :name',
            ExpressionAttributeValues={':name': business_name}
        )
        return response.get('Items', [])
    
    def create_waiting(self, business_name, number_of_customers, detail_attribute, phone_number):
        waiting_id = str(uuid.uuid4())
        item = {
            'business_name': business_name,
            'waiting_id': waiting_id,
            'date_created': '2023-06-04',  # Example: Set the date_created attribute
            'number_of_customers': number_of_customers,
            'detail_attribute': detail_attribute,
            'phone_number': phone_number,
            'status': 'waiting',
        }
        self.table.put_item(Item=item)
        return item
    
    def update_waiting(self, business_name, waiting_id, update_expression, expression_attribute_values):
        self.table.update_item(
            Key={'business_name': business_name, 'waiting_id': waiting_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
    
    def delete_waiting(self, business_name, waiting_id):
        self.table.delete_item(Key={'business_name': business_name, 'waiting_id': waiting_id})