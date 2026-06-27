from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.database.models import Cliente, User
from app.helpers import response_success, response_error

clientes_bp = Blueprint('clientes', __name__)


def serialize_cliente(cliente):
    """Serialize cliente to dict."""
    return {
        'id': cliente.id,
        'nome': cliente.nome,
        'email': cliente.email,
        'responsavel': cliente.responsavel,
        'created_at': cliente.created_at.isoformat() if hasattr(cliente, 'created_at') else None,
    }


@clientes_bp.route('', methods=['GET'])
@jwt_required()
def get_clientes(current_user_id):
    """List all clientes (paginated)."""
    # Verify user exists
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Cliente.query.order_by(Cliente.id.desc())
    paginated = query.paginate(page=max(1, page), per_page=min(100, max(1, per_page)), error_out=False)
    
    return response_success({
        'items': [serialize_cliente(c) for c in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'per_page': per_page,
    })


@clientes_bp.route('/<int:cliente_id>', methods=['GET'])
@jwt_required()
def get_cliente(current_user_id, cliente_id):
    """Get a specific cliente by ID."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return response_error('Cliente não encontrado', 404)

    return response_success(serialize_cliente(cliente))


@clientes_bp.route('', methods=['POST'])
@jwt_required()
def create_cliente(current_user_id):
    """Create a new cliente."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    data = request.get_json() or {}
    nome = (data.get('nome') or '').strip()

    if not nome:
        return response_error('Nome é obrigatório', 400)

    cliente = Cliente(
        nome=nome,
        email=(data.get('email') or '').strip() or None,
        responsavel=(data.get('responsavel') or '').strip() or None,
    )
    db.session.add(cliente)
    db.session.commit()

    return response_success(serialize_cliente(cliente), 'Cliente criado com sucesso', 201)


@clientes_bp.route('/<int:cliente_id>', methods=['PUT'])
@jwt_required()
def update_cliente(current_user_id, cliente_id):
    """Update a cliente."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return response_error('Cliente não encontrado', 404)

    data = request.get_json() or {}
    
    if 'nome' in data:
        nome = (data.get('nome') or '').strip()
        if not nome:
            return response_error('Nome é obrigatório', 400)
        cliente.nome = nome
    
    if 'email' in data:
        cliente.email = (data.get('email') or '').strip() or None
    
    if 'responsavel' in data:
        cliente.responsavel = (data.get('responsavel') or '').strip() or None

    db.session.commit()

    return response_success(serialize_cliente(cliente), 'Cliente atualizado com sucesso')


@clientes_bp.route('/<int:cliente_id>', methods=['DELETE'])
@jwt_required()
def delete_cliente(current_user_id, cliente_id):
    """Delete a cliente."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return response_error('Cliente não encontrado', 404)

    db.session.delete(cliente)
    db.session.commit()

    return response_success(None, 'Cliente removido com sucesso')
