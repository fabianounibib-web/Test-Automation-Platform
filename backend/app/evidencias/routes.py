from flask import Blueprint, request, jsonify

evidencias_bp = Blueprint('evidencias', __name__)


@evidencias_bp.route('/<int:id>', methods=['GET'])
def get_evidencia(id):
    return jsonify({'id': id}), 200


@evidencias_bp.route('/upload', methods=['POST'])
def upload_evidencia():
    return jsonify({'msg': 'upload not implemented'}), 201
