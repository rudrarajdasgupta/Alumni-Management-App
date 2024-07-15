from flask_restx import fields
from ..api import api
from .timestamp_fields import timestamp_fields

service_request_request_model = api.model('ServiceRequestRequest', {
    'raised_by': fields.String(required=True, description='The username who raised the request'),
    'assigned_to': fields.String(description='The username who is assigned to the request'),
    'assigned_by': fields.String(description='The username who assigned the request'),
    'status': fields.String(description='The status of the request', enum=['UNASSIGNED', 'UNRESOLVED', 'RESOLVED']),
    'subject': fields.String(required=True, description='The subject of the service request'),
    'content': fields.String(required=True, description='The content of the service request'),
    'attachment_url': fields.String(description='URL to the attachment'),
    'employee_id': fields.Integer(required=True, description='ID of the employee who raised the request')
})

service_request_response_model = api.model('ServiceRequestResponse', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of the service request'),
    'raised_by': fields.String(required=True, description='The username who raised the request'),
    'assigned_to': fields.String(description='The username who is assigned to the request'),
    'assigned_by': fields.String(description='The username who assigned the request'),
    'status': fields.String(description='The status of the request', enum=['UNASSIGNED', 'UNRESOLVED', 'RESOLVED']),
    'subject': fields.String(required=True, description='The subject of the service request'),
    'content': fields.String(required=True, description='The content of the service request'),
    'attachment_url': fields.String(description='URL to the attachment'),
    'employee_id': fields.Integer(required=True, description='ID of the employee who raised the request'),
    **timestamp_fields
})