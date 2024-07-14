from flask import request, jsonify
from flask_restx import Resource, Namespace
from ..extensions import db, bcrypt
from ..models import Admin, HR, Employee, Company
from ..schemas import user_request_model, user_response_model, register_request_model, hr_request_model, hr_response_model, admin_request_model, admin_response_model, employee_request_model, employee_response_model, company_request_model, company_response_model
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..utils import token_required, is_admin_or_hr, is_admin, is_hr
from datetime import datetime, timezone


# Create namespaces
company_namespace = Namespace('companies', description='Company related operations')

def register_company_routes(api):
    api.add_namespace(company_namespace)

# CRUD Endpoints for Company
@company_namespace.route('')
class CompanyList(Resource):
    @token_required
    @company_namespace.marshal_list_with(company_response_model)
    @company_namespace.doc(description='Get the list of all companies')
    def get(self):
        return Company.query.all()


    @company_namespace.expect(company_request_model, validate=True)
    @company_namespace.doc(description='Create a new company')
    def post(self):
        data = request.get_json()
        new_company = Company(name=data['name'])
        db.session.add(new_company)
        db.session.commit()
        return {'message': 'Company created successfully'}, 201

@company_namespace.route('/<int:id>')
class CompanyResource(Resource):
    @token_required
    @company_namespace.marshal_with(company_response_model)
    @company_namespace.doc(description='Get details of a specific company by ID')
    def get(self, id):
        return Company.query.get_or_404(id)

    @token_required
    @company_namespace.expect(company_request_model, validate=True)
    @company_namespace.doc(description='Update details of a specific company by ID')
    def put(self, id):
        if not is_admin():
            return {'message': 'Admin access required'}, 403
        data = request.get_json()
        company = Company.query.get_or_404(id)
        company.name = data['name']
        db.session.commit()
        return {'message': 'Company updated successfully'}

    @token_required
    @company_namespace.doc(description='Delete a specific company by ID')
    def delete(self, id):
        if not is_admin():
            return {'message': 'Admin access required'}, 403
        company = Company.query.get_or_404(id)
        db.session.delete(company)
        db.session.commit()
        return {'message': 'Company deleted successfully'}

