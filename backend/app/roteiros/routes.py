from flask import Blueprint, request, jsonify

roteiros_bp = Blueprint('roteiros', __name__)


@roteiros_bp.route('', methods=['GET'])
def get_roteiros():
    return jsonify([]), 200


@roteiros_bp.route('/upload', methods=['POST'])
def upload_roteiro():
    # placeholder for file upload
    return jsonify({'msg': 'upload not implemented'}), 201
