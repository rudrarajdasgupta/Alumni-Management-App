from flask import request, jsonify
from flask_restx import Resource, Namespace
from ..extensions import db
from ..models.service_request import ServiceRequest
from ..schemas.service_request_schemas import service_request_request_model, service_request_response_model
from flask_jwt_extended import jwt_required
from ..utils.utils import token_required

service_request_namespace = Namespace('service_requests', description='Service Request related operations')

def register_service_request_routes(api):
    api.add_namespace(service_request_namespace)

@service_request_namespace.route('')
class ServiceRequestList(Resource):
    @token_required
    @service_request_namespace.marshal_list_with(service_request_response_model)
    @service_request_namespace.doc(description='Get the list of all Service Requests')
    def get(self):
        return ServiceRequest.query.all()

    @token_required
    @service_request_namespace.expect(service_request_request_model, validate=True)
    @service_request_namespace.doc(description='Create a new Service Request')
    def post(self):
        data = request.get_json()
        new_request = ServiceRequest(
            raised_by=data['raised_by'],
            assigned_to=data.get('assigned_to'),
            assigned_by=data.get('assigned_by'),
            status=data.get('status', 'UNASSIGNED'),
            subject=data['subject'],
            content=data['content'],
            attachment_url=data.get('attachment_url'),
            employee_id=data['employee_id']
        )
        db.session.add(new_request)
        db.session.commit()
        return {'message': 'Service Request created successfully'}, 201

@service_request_namespace.route('/<int:id>')
class ServiceRequestResource(Resource):
    @token_required
    @service_request_namespace.marshal_with(service_request_response_model)
    @service_request_namespace.doc(description='Get details of a specific Service Request by ID')
    def get(self, id):
        request = ServiceRequest.query.get_or_404(id)
        return request

    @token_required
    @service_request_namespace.expect(service_request_request_model, validate=True)
    @service_request_namespace.doc(description='Update details of a specific Service Request by ID')
    def put(self, id):
        data = request.get_json()
        request = ServiceRequest.query.get_or_404(id)
        request.raised_by = data['raised_by']
        request.assigned_to = data.get('assigned_to', request.assigned_to)
        request.assigned_by = data.get('assigned_by', request.assigned_by)
        request.status = data.get('status', request.status)
        request.subject = data['subject']
        request.content = data['content']
        request.attachment_url = data.get('attachment_url', request.attachment_url)
        request.employee_id = data['employee_id']
        db.session.commit()
        return {'message': 'Service Request updated successfully'}

    @token_required
    @service_request_namespace.doc(description='Delete a specific Service Request by ID')
    def delete(self, id):
        request = ServiceRequest.query.get_or_404(id)
        db.session.delete(request)
        db.session.commit()
        return {'message': 'Service Request deleted successfully'}