from datetime import datetime
from flask import request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.utils import token_required, is_admin_or_hr
from ..utils.file_management_dynamodb_utils import create_dynamodb_table, upload_file_url, get_files, update_file, delete_file
from ..schemas.file_schemas import file_upload_request_model, file_response_model, file_update_request_model

file_namespace = Namespace('files', description='File operations')

def register_file_management_routes(api):
    api.add_namespace(file_namespace)

@file_namespace.route('/create-table')
class CreateTable(Resource):
    @file_namespace.doc(description='Create DynamoDB table')
    def post(self):
        response = create_dynamodb_table()
        return response, 201

@file_namespace.route('/upload-url')
class UploadURL(Resource):
    @jwt_required()
    @file_namespace.expect(file_upload_request_model, validate=True)
    @file_namespace.marshal_with(file_response_model, code=201)
    @file_namespace.doc(security='Bearer', description='Upload file URL')
    def post(self):
        if not is_admin_or_hr():
            return {'message': 'Admin or HR access required'}, 403

        data = request.get_json()
        company_id = data.get('company_id')
        employee_id = data.get('employee_id')
        file_url = data.get('file_url')
        file_type = data.get('file_type')
        uploaded_by = get_jwt_identity().get('username')

        if not company_id or not employee_id or not file_url or not file_type:
            return {'message': 'Missing required fields'}, 400

        try:
            upload_file_url(company_id, employee_id, file_url, file_type, uploaded_by)
        except ValueError as e:
            return {'message': str(e)}, 400

        return get_files(company_id, employee_id), 201

@file_namespace.route('/<string:company_id>/<string:employee_id>')
class FileResource(Resource):
    @jwt_required()
    @file_namespace.marshal_with(file_response_model, code=200)
    @file_namespace.doc(security='Bearer', description='Get file details')
    def get(self, company_id, employee_id):
        try:
            item = get_files(company_id, employee_id)
        except ValueError as e:
            return {'message': str(e)}, 404
        return item, 200

    @jwt_required()
    @file_namespace.expect(file_update_request_model, validate=True)
    @file_namespace.marshal_with(file_response_model, code=200)
    @file_namespace.doc(security='Bearer', description='Update file details')
    def put(self, company_id, employee_id):
        if not is_admin_or_hr():
            return {'message': 'Admin or HR access required'}, 403

        data = request.get_json()
        file_url = data.get('file_url')
        new_file_type = data.get('file_type')
        updated_by = get_jwt_identity().get('username')
        index = data.get('index')

        if not file_url or not new_file_type or index is None:
            return {'message': 'Missing required fields'}, 400

        try:
            update_file(company_id, employee_id, file_url, new_file_type, updated_by, index)
        except ValueError as e:
            return {'message': str(e)}, 400

        return get_files(company_id, employee_id), 200

    @jwt_required()
    @file_namespace.doc(security='Bearer', description='Delete file details')
    def delete(self, company_id, employee_id):
        if not is_admin_or_hr():
            return {'message': 'Admin or HR access required'}, 403

        index = request.args.get('index')

        if index is None:
            return {'message': 'Missing required fields'}, 400

        try:
            delete_file(company_id, employee_id, int(index))
        except ValueError as e:
            return {'message': str(e)}, 404

        return {'message': 'File deleted successfully'}, 200