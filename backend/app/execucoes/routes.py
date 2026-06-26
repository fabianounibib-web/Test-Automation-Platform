from flask import Blueprint, request, jsonify

execucoes_bp = Blueprint('execucoes', __name__)


@execucoes_bp.route('', methods=['GET'])
def get_execucoes():
    return jsonify([]), 200


@execucoes_bp.route('/<int:id>', methods=['GET'])
def get_execucao(id):
    return jsonify({'id': id}), 200
