from flask import Blueprint, request, jsonify

clientes_bp = Blueprint('clientes', __name__)


@clientes_bp.route('', methods=['GET'])
def get_clientes():
    return jsonify([]), 200


@clientes_bp.route('', methods=['POST'])
def create_cliente():
    data = request.get_json() or {}
    return jsonify({'msg': 'not implemented'}), 201
