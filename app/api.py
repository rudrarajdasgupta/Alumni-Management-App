from flask_restx import Api
from flask import Blueprint

# Create blueprint
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# Define security settings
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
    }
}

# Create a single Api instance
api = Api(api_blueprint, version='1.0', title='Alumnux Core API', authorizations=authorizations, security='Bearer')

def register_apis(app):
    app.register_blueprint(api_blueprint)

    # Import and register namespaces after the app and blueprints are initialized
    from .routes.auth import register_auth_routes
    from .routes.company import register_company_routes
    from .routes.admin import register_admin_routes
    from .routes.hr import register_hr_routes
    from .routes.employee import register_employee_routes
    from .routes.file_management import register_file_management_routes
    from .routes.company_config import register_config_routes
    from .routes.service_request import register_service_request_routes
    from .routes.comment import register_comment_routes
    register_auth_routes(api)
    register_company_routes(api)
    register_admin_routes(api)
    register_hr_routes(api)
    register_employee_routes(api)
    register_file_management_routes(api)
    register_config_routes(api)
    register_service_request_routes(api)
    register_comment_routes(api)