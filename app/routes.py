from flask import request, jsonify
from flask_restx import Resource, Namespace
from .extensions import db, bcrypt
from .models import Admin, HR, Employee, Company
from .schemas import user_request_model, user_response_model, register_request_model, hr_request_model, hr_response_model, admin_request_model, admin_response_model, employee_request_model, employee_response_model, company_request_model, company_response_model
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .utils import token_required

# Create namespaces
auth_namespace = Namespace('auth', description='Authentication related operations')
admin_namespace = Namespace('admins', description='Admin related operations')
hr_namespace = Namespace('hrs', description='HR related operations')
employee_namespace = Namespace('employees', description='Employee related operations')
company_namespace = Namespace('companies', description='Company related operations')

def register_routes(api):
    api.add_namespace(auth_namespace)
    api.add_namespace(admin_namespace)
    api.add_namespace(hr_namespace)
    api.add_namespace(employee_namespace)
    api.add_namespace(company_namespace)

def is_admin_or_hr():
    identity = get_jwt_identity()
    return identity and (identity['role'] == 'admin' or identity['role'] == 'hr')

def is_admin():
    identity = get_jwt_identity()
    return identity and identity['role'] == 'admin'

@auth_namespace.route('/register')
class Register(Resource):
    @auth_namespace.expect(register_request_model, validate=True)
    @auth_namespace.doc(description='Register a new user (Admin, HR, or Employee)')
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        company_id = data.get('company_id')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if role == 'admin':
            new_user = Admin(username=username, email=email, password=hashed_password, company_id=company_id)
        elif role == 'hr':
            new_user = HR(username=username, email=email, password=hashed_password, company_id=company_id)
        elif role == 'employee':
            new_user = Employee(username=username, email=email, password=hashed_password, company_id=company_id)
        else:
            return {'message': 'Invalid role specified'}, 400

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(user_request_model, validate=True)
    @auth_namespace.doc(description='Login to get a JWT token')
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = Admin.query.filter_by(username=username).first() or HR.query.filter_by(username=username).first() or Employee.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity={'username': user.username, 'role': user.__class__.__name__.lower()})
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

# CRUD Endpoints for Company
@company_namespace.route('')
class CompanyList(Resource):
    @token_required
    @company_namespace.marshal_list_with(company_response_model)
    @company_namespace.doc(description='Get the list of all companies')
    def get(self):
        return Company.query.all()

    @token_required
    @company_namespace.expect(company_request_model, validate=True)
    @company_namespace.doc(description='Create a new company')
    def post(self):
        if not is_admin():
            return {'message': 'Admin access required'}, 403
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

# CRUD Endpoints for Admin
@admin_namespace.route('')
class AdminList(Resource):
    @token_required
    @admin_namespace.marshal_list_with(admin_response_model)
    @admin_namespace.doc(description='Get the list of all admins')
    def get(self):
        return Admin.query.all()

    @token_required
    @admin_namespace.expect(admin_request_model, validate=True)
    @admin_namespace.doc(description='Create a new admin')
    def post(self):
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_admin = Admin(username=data['username'], email=data['email'], password=hashed_password, company_id=data['company_id'])
        db.session.add(new_admin)
        db.session.commit()
        return {'message': 'Admin created successfully'}, 201

@admin_namespace.route('/<int:id>')
class AdminResource(Resource):
    @token_required
    @admin_namespace.marshal_with(admin_response_model)
    @admin_namespace.doc(description='Get details of a specific admin by ID')
    def get(self, id):
        admin = Admin.query.get_or_404(id)
        return admin

    @token_required
    @admin_namespace.expect(admin_request_model, validate=True)
    @admin_namespace.doc(description='Update details of a specific admin by ID')
    def put(self, id):
        data = request.get_json()
        admin = Admin.query.get_or_404(id)
        admin.username = data['username']
        admin.email = data['email']
        admin.company_id = data['company_id']
        if 'password' in data:
            admin.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        db.session.commit()
        return {'message': 'Admin updated successfully'}

    @token_required
    @admin_namespace.doc(description='Delete a specific admin by ID')
    def delete(self, id):
        admin = Admin.query.get_or_404(id)
        db.session.delete(admin)
        db.session.commit()
        return {'message': 'Admin deleted successfully'}

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
        if not is_admin_or_hr():
            return {'message': 'Admin or HR access required'}, 403
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_employee = Employee(
            username=data['username'],
            email=data['email'],
            password=hashed_password,
            company_id=data['company_id'],
            joining_date=data.get('joining_date', datetime.utcnow()),
            last_working_date=data.get('last_working_date')
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
        if not is_admin_or_hr():
            return {'message': 'Admin or HR access required'}, 403
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
        if not is_admin_or_hr():
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
