from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    # placeholder: validate user and return token
    return jsonify({'access_token': 'dummy-token'}), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    return jsonify({'msg': 'register not implemented'}), 201
