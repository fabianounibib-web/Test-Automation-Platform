from flask import Blueprint, request, jsonify
from app import db
from app.database.models import Cliente

clientes_bp = Blueprint('clientes', __name__)


@clientes_bp.route('', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return jsonify([
        {
            'id': cliente.id,
            'nome': cliente.nome,
            'email': cliente.email,
            'responsavel': cliente.responsavel
        }
        for cliente in clientes
    ]), 200


@clientes_bp.route('', methods=['POST'])
def create_cliente():
    data = request.get_json() or {}
    nome = (data.get('nome') or '').strip()
    if not nome:
        return jsonify({'error': 'nome é obrigatório'}), 400

    cliente = Cliente(
        nome=nome,
        email=(data.get('email') or '').strip() or None,
        responsavel=(data.get('responsavel') or '').strip() or None
    )
    db.session.add(cliente)
    db.session.commit()

    return jsonify({
        'id': cliente.id,
        'nome': cliente.nome,
        'email': cliente.email,
        'responsavel': cliente.responsavel
    }), 201
