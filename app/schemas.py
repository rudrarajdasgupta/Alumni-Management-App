from flask_restx import fields
from .api import api

# Timestamp fields for response models
timestamp_fields = {
    'created_at': fields.DateTime(readOnly=True, description='The time this record was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The time this record was last updated')
}

# Models for requests
user_request_model = api.model('UserRequest', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'password': fields.String(required=True, description='The password')
})

register_request_model = api.model('RegisterRequest', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'password': fields.String(required=True, description='The password'),
    'role': fields.String(required=True, description='The role (admin, hr, employee)'),
    'company_id': fields.Integer(required=True, description='The company ID')
})

admin_request_model = api.model('AdminRequest', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'company_id': fields.Integer(required=True, description='The company ID'),
    'password': fields.String(description='The password')
})

hr_request_model = api.model('HRRequest', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'company_id': fields.Integer(required=True, description='The company ID'),
    'password': fields.String(description='The password')
})

employee_request_model = api.model('EmployeeRequest', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'company_id': fields.Integer(required=True, description='The company ID'),
    'password': fields.String(description='The password'),
    'joining_date': fields.DateTime(description='The joining date of the employee'),
    'last_working_date': fields.DateTime(description='The last working date of the employee')
})

company_request_model = api.model('CompanyRequest', {
    'name': fields.String(required=True, description='The name of the company')
})

# Models for responses
user_response_model = api.model('UserResponse', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    **timestamp_fields
})

admin_response_model = api.model('AdminResponse', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an admin'),
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'company_id': fields.Integer(required=True, description='The company ID'),
    **timestamp_fields
})

hr_response_model = api.model('HRResponse', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an HR'),
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'company_id': fields.Integer(required=True, description='The company ID'),
    **timestamp_fields
})

employee_response_model = api.model('EmployeeResponse', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an employee'),
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'company_id': fields.Integer(required=True, description='The company ID'),
    'joining_date': fields.DateTime(required=True, description='The joining date of the employee'),
    'last_working_date': fields.DateTime(description='The last working date of the employee'),
    **timestamp_fields
})

company_response_model = api.model('CompanyResponse', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a company'),
    'name': fields.String(required=True, description='The name of the company'),
    **timestamp_fields
})