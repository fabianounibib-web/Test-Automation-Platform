"""Helper functions for standardized responses and common operations."""
from flask import jsonify


def response_success(data=None, message=None, status_code=200):
    """Return standardized success response."""
    payload = {
        'success': True,
        'data': data,
    }
    if message:
        payload['message'] = message
    return jsonify(payload), status_code


def response_error(message, status_code=400, error_code=None):
    """Return standardized error response."""
    payload = {
        'success': False,
        'error': message,
    }
    if error_code:
        payload['error_code'] = error_code
    return jsonify(payload), status_code
