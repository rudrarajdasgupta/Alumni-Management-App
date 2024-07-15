from datetime import datetime
from flask import current_app

VALID_FILE_TYPES = ["FORM16", "PAYSLIP", "APPOINTMENT_LETTER", "RELIEVING_LETTER", "APPRAISAL"]

def create_dynamodb_table():
    table_name = current_app.config['DYNAMODB_FILE_MANAGEMENT_TABLE_NAME']
    existing_tables = current_app.dynamodb.tables.all()
    if table_name in [table.name for table in existing_tables]:
        return {'message': 'Table already exists'}

    table = current_app.dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'company_id', 'KeyType': 'HASH'},  # Partition key
            {'AttributeName': 'employee_id', 'KeyType': 'RANGE'}  # Sort key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'company_id', 'AttributeType': 'S'},
            {'AttributeName': 'employee_id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.wait_until_exists()
    return {'message': 'Table created successfully'}

def upload_file_url(company_id, employee_id, file_url, file_type, uploaded_by):
    if file_type not in VALID_FILE_TYPES:
        raise ValueError('Invalid file type')

    uploaded_date = datetime.utcnow().isoformat()

    table = current_app.dynamodb_file_management_table
    response = table.get_item(
        Key={
            'company_id': company_id,
            'employee_id': employee_id
        }
    )
    item = response.get('Item', {})
    
    # Add the new file entry to the existing or new list
    file_entries = item.get('files', [])
    file_entries.append({
        'file_url': file_url,
        'file_type': file_type,
        'uploaded_by': uploaded_by,
        'uploaded_date': uploaded_date
    })

    table.put_item(
        Item={
            'company_id': company_id,
            'employee_id': employee_id,
            'files': file_entries
        }
    )

def get_files(company_id, employee_id):
    response = current_app.dynamodb_file_management_table.get_item(
        Key={
            'company_id': company_id,
            'employee_id': employee_id
        }
    )
    item = response.get('Item')
    if not item:
        raise ValueError('Files not found')
    return item

def update_file(company_id, employee_id, file_url, new_file_type, updated_by, index):
    if new_file_type not in VALID_FILE_TYPES:
        raise ValueError('Invalid file type')

    response = current_app.dynamodb_file_management_table.get_item(
        Key={
            'company_id': company_id,
            'employee_id': employee_id
        }
    )
    item = response.get('Item')
    if not item or 'files' not in item or index >= len(item['files']):
        raise ValueError('File not found')

    updated_date = datetime.utcnow().isoformat()

    item['files'][index] = {
        'file_url': file_url,
        'file_type': new_file_type,
        'uploaded_by': updated_by,
        'uploaded_date': updated_date
    }

    current_app.dynamodb_table.put_item(Item=item)

def delete_file(company_id, employee_id, index):
    response = current_app.dynamodb_file_management_table.get_item(
        Key={
            'company_id': company_id,
            'employee_id': employee_id
        }
    )
    item = response.get('Item')
    if not item or 'files' not in item or index >= len(item['files']):
        raise ValueError('File not found')

    del item['files'][index]

    current_app.dynamodb_table.put_item(Item=item)