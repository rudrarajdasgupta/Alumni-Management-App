from flask_restx import fields
from ..api import api
from .timestamp_fields import timestamp_fields

admin_request_model = api.model('AdminRequest', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'company_id': fields.Integer(required=True, description='The company ID'),
    'password': fields.String(description='The password')
})

admin_response_model = api.model('AdminResponse', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an admin'),
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'company_id': fields.Integer(required=True, description='The company ID'),
    **timestamp_fields
})