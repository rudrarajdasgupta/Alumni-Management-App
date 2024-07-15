from flask_restx import fields
from ..api import api
from .timestamp_fields import timestamp_fields

company_request_model = api.model('CompanyRequest', {
    'name': fields.String(required=True, description='The name of the company')
})

company_response_model = api.model('CompanyResponse', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a company'),
    'name': fields.String(required=True, description='The name of the company'),
    **timestamp_fields
})