from waitinglist_table import WaitingTable

class DynamoDBClient:
    def __init__(self, table_name):
        self.waiting_table = WaitingTable(table_name)
    
    def get_waiting_by_id(self, business_name, waiting_id):
        return self.waiting_table.get_waiting_by_id(business_name, waiting_id)
    
    def get_waitings_by_business_name(self, business_name):
        return self.waiting_table.get_waitings_by_business_name(business_name)
    
    # TODO: check data type of all attributes
    def create_waiting(self, business_name, number_of_customers, detail_attribute, phone_number):
        return self.waiting_table.create_waiting(business_name, number_of_customers, detail_attribute, phone_number)
    
    def update_waiting(self, business_name, waiting_id, update_expression, expression_attribute_values):
        self.waiting_table.update_waiting(business_name, waiting_id, update_expression, expression_attribute_values)
    
    def delete_waiting(self, business_name, waiting_id):
        self.waiting_table.delete_waiting(business_name, waiting_id)