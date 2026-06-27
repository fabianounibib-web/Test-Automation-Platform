from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.database.models import Conector, User
from app.helpers import response_success, response_error

conectores_bp = Blueprint('conectores', __name__)


def serialize_conector(conector, include_steps=True):
    """Serialize conector to dict."""
    payload = {
        'id': conector.id,
        'nome': conector.nome,
        'descricao': conector.descricao,
        'url_base': conector.url_base,
        'ambiente': conector.ambiente,
        'status': conector.status,
        'versao': conector.versao,
        'created_at': conector.created_at.isoformat() if conector.created_at else None,
        'updated_at': conector.updated_at.isoformat() if conector.updated_at else None,
    }
    if include_steps:
        payload['steps'] = conector.steps or []
        payload['credenciais_ref'] = conector.credenciais_ref or {}
    return payload


@conectores_bp.route('', methods=['GET'])
@jwt_required()
def get_conectores(current_user_id):
    """List all conectores (systems/web targets)."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Conector.query.order_by(Conector.id.desc())
    paginated = query.paginate(page=max(1, page), per_page=min(100, max(1, per_page)), error_out=False)
    
    return response_success({
        'items': [serialize_conector(c, include_steps=False) for c in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'per_page': per_page,
    })


@conectores_bp.route('/<int:conector_id>', methods=['GET'])
@jwt_required()
def get_conector(current_user_id, conector_id):
    """Get a specific conector by ID."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    conector = Conector.query.get(conector_id)
    if not conector:
        return response_error('Sistema não encontrado', 404)

    return response_success(serialize_conector(conector))


@conectores_bp.route('', methods=['POST'])
@jwt_required()
def create_conector(current_user_id):
    """Create a new conector (web system)."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    data = request.get_json() or {}
    nome = (data.get('nome') or '').strip()
    url_base = (data.get('url_base') or '').strip()

    if not nome or not url_base:
        return response_error('Nome e URL são obrigatórios', 400)

    conector = Conector(
        nome=nome,
        descricao=(data.get('descricao') or '').strip() or None,
        url_base=url_base,
        tipo=data.get('tipo', 'web'),
        ambiente=data.get('ambiente', 'desenvolvimento'),
        status=data.get('status', 'draft'),
        credenciais_ref=data.get('credenciais_ref', {}),
    )
    db.session.add(conector)
    db.session.commit()

    return response_success(serialize_conector(conector), 'Sistema criado com sucesso', 201)


@conectores_bp.route('/<int:conector_id>', methods=['PUT'])
@jwt_required()
def update_conector(current_user_id, conector_id):
    """Update a conector."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    conector = Conector.query.get(conector_id)
    if not conector:
        return response_error('Sistema não encontrado', 404)

    data = request.get_json() or {}
    
    if 'nome' in data:
        nome = (data.get('nome') or '').strip()
        if not nome:
            return response_error('Nome é obrigatório', 400)
        conector.nome = nome
    
    if 'url_base' in data:
        url_base = (data.get('url_base') or '').strip()
        if not url_base:
            return response_error('URL é obrigatória', 400)
        conector.url_base = url_base
    
    if 'descricao' in data:
        conector.descricao = (data.get('descricao') or '').strip() or None
    
    if 'ambiente' in data:
        conector.ambiente = data.get('ambiente')
    
    if 'status' in data:
        conector.status = data.get('status')
    
    if 'credenciais_ref' in data:
        conector.credenciais_ref = data.get('credenciais_ref', {})
    
    conector.updated_at = datetime.utcnow()
    db.session.commit()

    return response_success(serialize_conector(conector), 'Sistema atualizado com sucesso')


@conectores_bp.route('/<int:conector_id>', methods=['DELETE'])
@jwt_required()
def delete_conector(current_user_id, conector_id):
    """Delete a conector."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    conector = Conector.query.get(conector_id)
    if not conector:
        return response_error('Sistema não encontrado', 404)

    db.session.delete(conector)
    db.session.commit()

    return response_success(None, 'Sistema removido com sucesso')


@conectores_bp.route('/<int:conector_id>/steps', methods=['POST'])
@jwt_required()
def save_steps(current_user_id, conector_id):
    """Save automation steps for a conector (from recording)."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    conector = Conector.query.get(conector_id)
    if not conector:
        return response_error('Sistema não encontrado', 404)

    data = request.get_json() or {}
    steps = data.get('steps', [])

    if not isinstance(steps, list):
        return response_error('Steps deve ser uma lista', 400)

    conector.steps = steps
    conector.status = 'ativo'
    conector.updated_at = datetime.utcnow()
    db.session.commit()

    return response_success(serialize_conector(conector), 'Steps salvos com sucesso')


@conectores_bp.route('/<int:conector_id>/steps', methods=['GET'])
@jwt_required()
def get_steps(current_user_id, conector_id):
    """Get automation steps for a conector."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    conector = Conector.query.get(conector_id)
    if not conector:
        return response_error('Sistema não encontrado', 404)

    return response_success({
        'conector_id': conector.id,
        'nome': conector.nome,
        'url_base': conector.url_base,
        'steps': conector.steps or [],
        'credenciais_ref': conector.credenciais_ref or {},
    })
