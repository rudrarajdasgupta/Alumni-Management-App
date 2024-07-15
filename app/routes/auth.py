from flask import request
from flask_restx import Resource, Namespace
from ..extensions import db, bcrypt
from ..models.admin import Admin
from ..models.hr import HR
from ..models.employee import Employee
from ..schemas.user_schemas import user_request_model, register_request_model
from flask_jwt_extended import create_access_token

# Create namespaces
auth_namespace = Namespace('auth', description='Authentication related operations')

def register_auth_routes(api):
    api.add_namespace(auth_namespace)

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