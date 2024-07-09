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
api = Api(api_blueprint, version='1.0', title='Alumni Management API', description='API for managing alumni', authorizations=authorizations, security='Bearer')

def register_apis(app):
    app.register_blueprint(api_blueprint)

    # Import and register namespaces after the app and blueprints are initialized
    from .routes import register_routes
    register_routes(api)