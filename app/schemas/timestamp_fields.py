from flask_restx import fields
from ..api import api

timestamp_fields = {
    'created_at': fields.DateTime(readOnly=True, description='The time this record was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The time this record was last updated')
}