from flask_restx import fields
from ..api import api
from .timestamp_fields import timestamp_fields

employee_request_model = api.model('EmployeeRequest', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'company_id': fields.Integer(required=True, description='The company ID'),
    'password': fields.String(description='The password'),
    'joining_date': fields.DateTime(description='The joining date of the employee'),
    'last_working_date': fields.DateTime(description='The last working date of the employee')
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