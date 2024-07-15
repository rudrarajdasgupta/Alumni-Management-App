from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        return f(*args, **kwargs)
    return decorated

def is_admin_or_hr():
    identity = get_jwt_identity()
    return identity and (identity['role'] == 'admin' or identity['role'] == 'hr')

def is_admin():
    identity = get_jwt_identity()
    return identity and identity['role'] == 'admin'

def is_hr():
    identity = get_jwt_identity()
    return identity and (identity['role'] == 'hr')
