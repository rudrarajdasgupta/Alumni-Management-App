from flask_restx import fields
from ..api import api
from .timestamp_fields import timestamp_fields

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

user_response_model = api.model('UserResponse', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    **timestamp_fields
})