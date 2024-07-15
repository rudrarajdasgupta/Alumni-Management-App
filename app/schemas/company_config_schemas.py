from flask_restx import fields
from ..api import api

company_config_request_model = api.model('CompanyConfigRequest', {
    'company_id': fields.String(required=True, description='The company ID'),
    'naming_convention': fields.Raw(required=True, description='Regex for naming convention for each file type'),
    'support_hr_ids': fields.List(fields.String, required=True, description='List of HR IDs who will work in support'),
    'upload_hr_ids': fields.List(fields.String, required=True, description='List of HR IDs who have upload privilege'),
    'valid_file_types': fields.List(fields.String, required=True, description='List of valid file types')
})

company_config_response_model = api.model('CompanyConfigResponse', {
    'company_id': fields.String(required=True, description='The company ID'),
    'naming_convention': fields.Raw(required=True, description='Regex for naming convention for each file type'),
    'support_hr_ids': fields.List(fields.String, required=True, description='List of HR IDs who will work in support'),
    'upload_hr_ids': fields.List(fields.String, required=True, description='List of HR IDs who have upload privilege'),
    'valid_file_types': fields.List(fields.String, required=True, description='List of valid file types')
})