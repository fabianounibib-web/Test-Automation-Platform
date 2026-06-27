from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.database.models import CasoTeste, Roteiro, Conector, User
from app.helpers import response_success, response_error

testes_bp = Blueprint('testes', __name__)


def serialize_caso_teste(caso):
    """Serialize test case to dict."""
    return {
        'id': caso.id,
        'roteiro_id': caso.roteiro_id,
        'nome': caso.nome,
        'objetivo': caso.objetivo,
        'dados': caso.dados or {},
        'resultado_esperado': caso.resultado_esperado,
        'status': caso.status,
        'created_at': caso.created_at.isoformat() if hasattr(caso, 'created_at') else None,
    }


@testes_bp.route('', methods=['GET'])
@jwt_required()
def get_casos(current_user_id):
    """List all test cases (paginated, with filters)."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    roteiro_id = request.args.get('roteiro_id', type=int)
    status = request.args.get('status', type=str)
    
    query = CasoTeste.query
    
    if roteiro_id:
        query = query.filter_by(roteiro_id=roteiro_id)
    
    if status:
        query = query.filter_by(status=status)
    
    query = query.order_by(CasoTeste.id.desc())
    paginated = query.paginate(page=max(1, page), per_page=min(100, max(1, per_page)), error_out=False)
    
    return response_success({
        'items': [serialize_caso_teste(c) for c in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'per_page': per_page,
    })


@testes_bp.route('/<int:caso_id>', methods=['GET'])
@jwt_required()
def get_caso(current_user_id, caso_id):
    """Get a specific test case by ID."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    caso = CasoTeste.query.get(caso_id)
    if not caso:
        return response_error('Caso de teste não encontrado', 404)

    return response_success(serialize_caso_teste(caso))


@testes_bp.route('', methods=['POST'])
@jwt_required()
def create_caso(current_user_id):
    """Create a new test case."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    data = request.get_json() or {}
    nome = (data.get('nome') or '').strip()

    if not nome:
        return response_error('Nome é obrigatório', 400)

    roteiro_id = data.get('roteiro_id')
    if roteiro_id:
        roteiro = Roteiro.query.get(roteiro_id)
        if not roteiro:
            return response_error('Roteiro não encontrado', 404)

    caso = CasoTeste(
        roteiro_id=roteiro_id,
        nome=nome,
        objetivo=(data.get('objetivo') or '').strip() or None,
        dados=data.get('dados', {}),
        resultado_esperado=(data.get('resultado_esperado') or '').strip() or None,
        status=data.get('status', 'criado'),
    )
    db.session.add(caso)
    db.session.commit()

    return response_success(serialize_caso_teste(caso), 'Caso de teste criado com sucesso', 201)


@testes_bp.route('/<int:caso_id>', methods=['PUT'])
@jwt_required()
def update_caso(current_user_id, caso_id):
    """Update a test case."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    caso = CasoTeste.query.get(caso_id)
    if not caso:
        return response_error('Caso de teste não encontrado', 404)

    data = request.get_json() or {}
    
    if 'nome' in data:
        nome = (data.get('nome') or '').strip()
        if not nome:
            return response_error('Nome é obrigatório', 400)
        caso.nome = nome
    
    if 'objetivo' in data:
        caso.objetivo = (data.get('objetivo') or '').strip() or None
    
    if 'dados' in data:
        caso.dados = data.get('dados', {})
    
    if 'resultado_esperado' in data:
        caso.resultado_esperado = (data.get('resultado_esperado') or '').strip() or None
    
    if 'status' in data:
        caso.status = data.get('status')

    db.session.commit()

    return response_success(serialize_caso_teste(caso), 'Caso de teste atualizado com sucesso')


@testes_bp.route('/<int:caso_id>', methods=['DELETE'])
@jwt_required()
def delete_caso(current_user_id, caso_id):
    """Delete a test case."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    caso = CasoTeste.query.get(caso_id)
    if not caso:
        return response_error('Caso de teste não encontrado', 404)

    db.session.delete(caso)
    db.session.commit()

    return response_success(None, 'Caso de teste removido com sucesso')


@testes_bp.route('/<int:id>/executar', methods=['POST'])
def executar_caso(id):
    from app.tasks.execute_case import execute_case_task

    caso = CasoTeste.query.get(id)
    if not caso:
        return jsonify({'error': 'caso não encontrado'}), 404

    task = execute_case_task.delay(id)
    return jsonify({'task_id': task.id, 'status': 'queued'}), 202
