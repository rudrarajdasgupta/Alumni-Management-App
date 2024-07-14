from flask import request, jsonify
from flask_restx import Resource, Namespace
from ..extensions import db, bcrypt
from ..models import Admin, HR, Employee, Company
from ..schemas import user_request_model, user_response_model, register_request_model, hr_request_model, hr_response_model, admin_request_model, admin_response_model, employee_request_model, employee_response_model, company_request_model, company_response_model
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..utils import token_required
from datetime import datetime, timezone
from .company import company_namespace



# Create namespaces
hr_namespace = Namespace('hrs', description='HR related operations')

def register_hr_routes(api):
    api.add_namespace(hr_namespace)

def is_admin_or_hr():
    identity = get_jwt_identity()
    return identity and (identity['role'] == 'admin' or identity['role'] == 'hr')

def is_admin():
    identity = get_jwt_identity()
    return identity and identity['role'] == 'admin'


# CRUD Endpoints for HR
@hr_namespace.route('')
class HRList(Resource):
    @token_required
    @hr_namespace.marshal_list_with(hr_response_model)
    @hr_namespace.doc(description='Get the list of all HRs')
    def get(self):
        return HR.query.all()

    @token_required
    @hr_namespace.expect(hr_request_model, validate=True)
    @hr_namespace.doc(description='Create a new HR')
    def post(self):
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_hr = HR(username=data['username'], email=data['email'], password=hashed_password, company_id=data['company_id'])
        db.session.add(new_hr)
        db.session.commit()
        return {'message': 'HR created successfully'}, 201

@hr_namespace.route('/<int:id>')
class HRResource(Resource):
    @token_required
    @hr_namespace.marshal_with(hr_response_model)
    @hr_namespace.doc(description='Get details of a specific HR by ID')
    def get(self, id):
        hr = HR.query.get_or_404(id)
        return hr

    @token_required
    @hr_namespace.expect(hr_request_model, validate=True)
    @hr_namespace.doc(description='Update details of a specific HR by ID')
    def put(self, id):
        data = request.get_json()
        hr = HR.query.get_or_404(id)
        hr.username = data['username']
        hr.email = data['email']
        hr.company_id = data['company_id']
        if 'password' in data:
            hr.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        db.session.commit()
        return {'message': 'HR updated successfully'}

    @token_required
    @hr_namespace.doc(description='Delete a specific HR by ID')
    def delete(self, id):
        hr = HR.query.get_or_404(id)
        db.session.delete(hr)
        db.session.commit()
        return {'message': 'HR deleted successfully'}

@company_namespace.route('/<int:company_id>/hrs')
class HRByCompany(Resource):
    @token_required
    @hr_namespace.marshal_list_with(hr_response_model)
    @hr_namespace.doc(description='Get the list of all HRs by company ID')
    def get(self, company_id):
        return HR.query.filter_by(company_id=company_id).all()

