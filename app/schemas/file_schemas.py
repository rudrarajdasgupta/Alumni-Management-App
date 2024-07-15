from flask_restx import fields
from ..api import api

file_entry_model = api.model('FileEntry', {
    'file_url': fields.String(required=True, description='The URL of the file'),
    'file_type': fields.String(required=True, description='The type of the file', enum=["FORM16", "PAYSLIP", "APPOINTMENT_LETTER", "RELIEVING_LETTER", "APPRAISAL"]),
    'uploaded_by': fields.String(required=True, description='The username of the uploader'),
    'uploaded_date': fields.DateTime(required=True, description='The upload date of the file')
})

file_upload_request_model = api.model('FileUploadRequest', {
    'company_id': fields.String(required=True, description='The company ID'),
    'employee_id': fields.String(required=True, description='The employee ID'),
    'file_url': fields.String(required=True, description='The URL of the file'),
    'file_type': fields.String(required=True, description='The type of the file', enum=["FORM16", "PAYSLIP", "APPOINTMENT_LETTER", "RELIEVING_LETTER", "APPRAISAL"])
})

file_response_model = api.model('FileResponse', {
    'company_id': fields.String(required=True, description='The company ID'),
    'employee_id': fields.String(required=True, description='The employee ID'),
    'files': fields.List(fields.Nested(file_entry_model), description='List of file entries')
})

file_update_request_model = api.model('FileUpdateRequest', {
    'file_url': fields.String(required=True, description='The URL of the file'),
    'file_type': fields.String(required=True, description='The type of the file', enum=["FORM16", "PAYSLIP", "APPOINTMENT_LETTER", "RELIEVING_LETTER", "APPRAISAL"])
})