from datetime import datetime
from flask import request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import token_required, is_admin
from ..config_dynamodb_utils import create_config_table, get_company_config, update_company_config, delete_company_config
from ..schemas import company_config_request_model, company_config_response_model

config_namespace = Namespace('config', description='Company configuration operations')

def register_config_routes(api):
    api.add_namespace(config_namespace)

@config_namespace.route('/create-table')
class CreateConfigTable(Resource):
    @config_namespace.doc(description='Create DynamoDB configuration table')
    def post(self):
        response = create_config_table()
        return response, 201

@config_namespace.route('/')
class CompanyConfigList(Resource):
    @jwt_required()
    @config_namespace.expect(company_config_request_model, validate=True)
    @config_namespace.marshal_with(company_config_response_model, code=201)
    @config_namespace.doc(security='Bearer', description='Create company configuration')
    def post(self):
        if not is_admin():
            return {'message': 'Admin or HR access required'}, 403

        data = request.get_json()
        company_id = data.get('company_id')
        config = {
            'naming_convention': data.get('naming_convention'),
            'support_hr_ids': data.get('support_hr_ids'),
            'upload_hr_ids': data.get('upload_hr_ids'),
            'valid_file_types': data.get('valid_file_types')
        }

        try:
            update_company_config(company_id, config)
        except ValueError as e:
            return {'message': str(e)}, 400

        return get_company_config(company_id), 201

@config_namespace.route('/<string:company_id>')
class CompanyConfigResource(Resource):
    @jwt_required()
    @config_namespace.marshal_with(company_config_response_model, code=200)
    @config_namespace.doc(security='Bearer', description='Get company configuration')
    def get(self, company_id):
        try:
            config = get_company_config(company_id)
        except ValueError as e:
            return {'message': str(e)}, 404
        return config, 200

    @jwt_required()
    @config_namespace.expect(company_config_request_model, validate=True)
    @config_namespace.marshal_with(company_config_response_model, code=200)
    @config_namespace.doc(security='Bearer', description='Update company configuration')
    def put(self, company_id):
        if not is_admin():
            return {'message': 'Admin or HR access required'}, 403

        data = request.get_json()
        try:
            update_company_config(company_id, data)
        except ValueError as e:
            return {'message': str(e)}, 400

        return get_company_config(company_id), 200

    @jwt_required()
    @config_namespace.doc(security='Bearer', description='Delete company configuration')
    def delete(self, company_id):
        if not is_admin():
            return {'message': 'Admin or HR access required'}, 403

        try:
            delete_company_config(company_id)
        except ValueError as e:
            return {'message': str(e)}, 404

        return {'message': 'Company configuration deleted successfully'}, 200