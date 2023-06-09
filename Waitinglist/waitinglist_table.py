import boto3
import uuid
import datetime

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
    
    def get_today_waitings(self, business_name):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        response = self.table.scan(
            FilterExpression='business_name = :name AND date_created BETWEEN :start_date AND :end_date',
            ExpressionAttributeValues={
                ':name': business_name,
                ':start_date': f"{current_date} 00:00:00",
                ':end_date': f"{current_date} 23:59:59"
            }
        )
        return response.get('Items', [])
    
    def create_waiting(self, business_name, number_of_customers, detail_attribute, phone_number):
        waiting_id = str(uuid.uuid4())
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item = {
            'business_name': business_name,
            'waiting_id': waiting_id,
            'date_created': current_time,  # Example: Set the date_created attribute
            'number_of_customers': int(number_of_customers),
            'detail_attribute': detail_attribute,
            'phone_number': str(phone_number),
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