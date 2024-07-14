from flask import request, jsonify
from flask_restx import Resource, Namespace
from ..extensions import db, bcrypt
from ..models import Admin, HR, Employee, Company
from ..schemas import user_request_model, user_response_model, register_request_model, hr_request_model, hr_response_model, admin_request_model, admin_response_model, employee_request_model, employee_response_model, company_request_model, company_response_model
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..utils import token_required, is_admin_or_hr, is_admin, is_hr
from datetime import datetime, timezone
from .company import company_namespace

# Create namespaces
employee_namespace = Namespace('employees', description='Employee related operations')

def register_employee_routes(api):
    api.add_namespace(employee_namespace)

# CRUD Endpoints for Employee
@employee_namespace.route('')
class EmployeeList(Resource):
    @token_required
    @employee_namespace.marshal_list_with(employee_response_model)
    @employee_namespace.doc(description='Get the list of all employees')
    def get(self):
        return Employee.query.all()

    @token_required
    @employee_namespace.expect(employee_request_model, validate=True)
    @employee_namespace.doc(description='Create a new employee')
    def post(self):
        if not is_hr():
            return {'message': 'HR access required'}, 403
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        identity=get_jwt_identity()
        new_employee = Employee(
            username=data['username'],
            email=data['email'],
            password=hashed_password,
            company_id=data['company_id'],
            created_by=identity["id"],
            joining_date= datetime.strptime(data["joining_date"], '%Y-%m-%d'),
            last_working_date=datetime.strptime(data["last_working_date"], '%Y-%m-%d')
        )
        db.session.add(new_employee)
        db.session.commit()
        return {'message': 'Employee created successfully'}, 201

@employee_namespace.route('/<int:id>')
class EmployeeResource(Resource):
    @token_required
    @employee_namespace.marshal_with(employee_response_model)
    @employee_namespace.doc(description='Get details of a specific employee by ID')
    def get(self, id):
        employee = Employee.query.get_or_404(id)
        return employee

    @token_required
    @employee_namespace.expect(employee_request_model, validate=True)
    @employee_namespace.doc(description='Update details of a specific employee by ID')
    def put(self, id):
        if not is_hr():
            return {'message': 'HR access required'}, 403
        data = request.get_json()
        employee = Employee.query.get_or_404(id)
        employee.username = data['username']
        employee.email = data['email']
        employee.company_id = data['company_id']
        employee.joining_date = data.get('joining_date', employee.joining_date)
        employee.last_working_date = data.get('last_working_date', employee.last_working_date)
        if 'password' in data:
            employee.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        db.session.commit()
        return {'message': 'Employee updated successfully'}

    @token_required
    @employee_namespace.doc(description='Delete a specific employee by ID')
    def delete(self, id):
        if not is_hr():
            return {'message': 'Admin or HR access required'}, 403
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return {'message': 'Employee deleted successfully'}

@company_namespace.route('/<int:company_id>/employees')
class EmployeesByCompany(Resource):
    @token_required
    @employee_namespace.marshal_list_with(employee_response_model)
    @employee_namespace.doc(description='Get the list of all employees by company ID')
    def get(self, company_id):
        return Employee.query.filter_by(company_id=company_id).all()
