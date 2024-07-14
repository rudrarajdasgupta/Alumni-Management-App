from datetime import datetime
from flask import current_app

def create_config_table():
    table_name = current_app.config['DYNAMODB_CONFIG_TABLE_NAME']
    existing_tables = current_app.dynamodb.tables.all()
    if table_name in [table.name for table in existing_tables]:
        return {'message': 'Configuration table already exists'}

    table = current_app.dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'company_id', 'KeyType': 'HASH'}  # Partition key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'company_id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.wait_until_exists()
    return {'message': 'Configuration table created successfully'}

def get_company_config(company_id):
    response = current_app.dynamodb_config_table.get_item(
        Key={'company_id': company_id}
    )
    return response.get('Item')

def update_company_config(company_id, config):
    current_app.dynamodb_config_table.put_item(
        Item={
            'company_id': company_id,
            'naming_convention': config.get('naming_convention'),
            'support_hr_ids': config.get('support_hr_ids', []),
            'upload_hr_ids': config.get('upload_hr_ids', []),
            'valid_file_types': config.get('valid_file_types', [])
        }
    )

def delete_company_config(company_id):
    current_app.dynamodb_config_table.delete_item(
        Key={'company_id': company_id}
    )