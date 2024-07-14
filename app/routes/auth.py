from flask import request, jsonify
from flask_restx import Resource, Namespace
from ..extensions import db, bcrypt
from ..models import Admin, HR, Employee, Company
from ..schemas import user_request_model, user_response_model, register_request_model, hr_request_model, hr_response_model, admin_request_model, admin_response_model, employee_request_model, employee_response_model, company_request_model, company_response_model
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..utils import token_required
from datetime import datetime, timezone


# Create namespaces
auth_namespace = Namespace('auth', description='Authentication related operations')

def register_auth_routes(api):
    api.add_namespace(auth_namespace)

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
            access_token = create_access_token(identity={'username': user.username, "id":user.id, 'role': user.__class__.__name__.lower()})
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

