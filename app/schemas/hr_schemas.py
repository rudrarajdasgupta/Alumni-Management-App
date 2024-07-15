from flask_restx import fields
from ..api import api
from .timestamp_fields import timestamp_fields

hr_request_model = api.model('HRRequest', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'company_id': fields.Integer(required=True, description='The company ID'),
    'password': fields.String(description='The password'),
    'upload_access': fields.Boolean(description='Upload access flag'),
    'support_flag': fields.Boolean(description='Support flag')
})

hr_response_model = api.model('HRResponse', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an HR'),
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'company_id': fields.Integer(required=True, description='The company ID'),
    'upload_access': fields.Boolean(description='Upload access flag'),
    'support_flag': fields.Boolean(description='Support flag'),
    **timestamp_fields
})