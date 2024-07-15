from flask_restx import fields
from ..api import api
from .timestamp_fields import timestamp_fields

comment_request_model = api.model('CommentRequest', {
    'comment': fields.String(required=True, description='The comment text'),
    'attachment_url': fields.String(description='URL to the attachment'),
    'servicerequest_id': fields.Integer(required=True, description='ID of the associated service request'),
    'employee_id': fields.Integer(required=True, description='ID of the employee who made the comment')
})

comment_response_model = api.model('CommentResponse', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of the comment'),
    'comment': fields.String(required=True, description='The comment text'),
    'attachment_url': fields.String(description='URL to the attachment'),
    'servicerequest_id': fields.Integer(required=True, description='ID of the associated service request'),
    'employee_id': fields.Integer(required=True, description='ID of the employee who made the comment'),
    **timestamp_fields
})