from flask import Blueprint, request, jsonify

logs_bp = Blueprint('logs', __name__)


@logs_bp.route('/<int:id>', methods=['GET'])
def get_log(id):
    return jsonify({'id': id}), 200


@logs_bp.route('/execucao/<int:execucao_id>', methods=['GET'])
def get_logs_by_execucao(execucao_id):
    return jsonify([]), 200
