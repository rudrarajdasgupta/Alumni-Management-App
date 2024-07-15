from flask import request
from flask_restx import Resource, Namespace
from ..extensions import db, bcrypt
from ..models.admin import Admin
from ..schemas.admin_schemas import admin_request_model, admin_response_model
from ..utils.utils import token_required

# Create namespaces
admin_namespace = Namespace('admins', description='Admin related operations')

def register_admin_routes(api):
    api.add_namespace(admin_namespace)

# CRUD Endpoints for Admin
@admin_namespace.route('')
class AdminList(Resource):
    @token_required
    @admin_namespace.marshal_list_with(admin_response_model)
    @admin_namespace.doc(description='Get the list of all admins')
    def get(self):
        return Admin.query.all()


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