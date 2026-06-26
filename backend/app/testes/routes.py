from flask import Blueprint, request, jsonify

testes_bp = Blueprint('testes', __name__)


@testes_bp.route('', methods=['GET'])
def get_casos():
    return jsonify([]), 200


@testes_bp.route('/<int:id>/executar', methods=['POST'])
def executar_caso(id):
    # placeholder to trigger execution
    return jsonify({'msg': f'executar caso {id} not implemented'}), 202
