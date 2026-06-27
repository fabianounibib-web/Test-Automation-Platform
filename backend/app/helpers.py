"""Helper functions for standardized responses and common operations."""
from flask import jsonify


def response_success(data=None, message=None, status_code=200):
    """Return standardized success response with compatibility for the MVP frontend and tests."""
    payload = {'success': True}
    if isinstance(data, dict):
        payload.update(data)
    elif data is not None:
        payload['value'] = data
    payload['data'] = data
    if message:
        payload['message'] = message
    return jsonify(payload), status_code


def response_error(message, status_code=400, error_code=None, details=None):
    """Return standardized error response."""
    payload = {
        'success': False,
        'error': message,
    }
    if error_code:
        payload['error_code'] = error_code
    if details is not None:
        payload['details'] = details
    return jsonify(payload), status_code
