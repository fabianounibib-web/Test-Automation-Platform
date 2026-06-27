from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.database.models import Execucao, CasoTeste, Conector, Log, Evidencia, User
from app.helpers import response_success, response_error

execucoes_bp = Blueprint('execucoes', __name__)


def serialize_execucao(execucao):
    """Serialize execution to dict."""
    return {
        'id': execucao.id,
        'caso_teste_id': execucao.caso_teste_id,
        'robo_id': execucao.robo_id,
        'status': execucao.status,
        'tempo': execucao.tempo,
        'rpa_id': execucao.rpa_id,
        'inicio': execucao.inicio.isoformat() if execucao.inicio else None,
        'fim': execucao.fim.isoformat() if execucao.fim else None,
        'created_at': execucao.created_at.isoformat() if execucao.created_at else None,
    }


@execucoes_bp.route('', methods=['GET'])
@jwt_required()
def get_execucoes(current_user_id):
    """List all executions (paginated, with filters)."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', type=str)
    caso_teste_id = request.args.get('caso_teste_id', type=int)
    
    query = Execucao.query
    
    if status:
        query = query.filter_by(status=status)
    
    if caso_teste_id:
        query = query.filter_by(caso_teste_id=caso_teste_id)
    
    query = query.order_by(Execucao.id.desc())
    paginated = query.paginate(page=max(1, page), per_page=min(100, max(1, per_page)), error_out=False)
    
    return response_success({
        'items': [serialize_execucao(e) for e in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'per_page': per_page,
    })


@execucoes_bp.route('/<int:execucao_id>', methods=['GET'])
@jwt_required()
def get_execucao(current_user_id, execucao_id):
    """Get a specific execution by ID."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    execucao = Execucao.query.get(execucao_id)
    if not execucao:
        return response_error('Execução não encontrada', 404)

    # Get logs count and evidence count
    logs_count = Log.query.filter_by(execucao_id=execucao_id).count()
    evidences_count = Evidencia.query.filter_by(execucao_id=execucao_id).count()

    result = serialize_execucao(execucao)
    result['logs_count'] = logs_count
    result['evidences_count'] = evidences_count

    return response_success(result)


@execucoes_bp.route('/casos/<int:caso_id>/execute', methods=['POST'])
@jwt_required()
def execute_caso(current_user_id, caso_id):
    """Start execution of a test case."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    caso = CasoTeste.query.get(caso_id)
    if not caso:
        return response_error('Caso de teste não encontrado', 404)

    # TODO: Add validation checks:
    # - Check if case has all required data
    # - Check if system is configured
    # - Check if RPA is available

    # Create execution record
    execucao = Execucao(
        caso_teste_id=caso_id,
        status='iniciando',
        inicio=datetime.utcnow(),
    )
    db.session.add(execucao)
    db.session.commit()

    # Enqueue Celery task for async execution
    try:
        # Import here to avoid circular import
        from app.tasks.execute_case import get_execute_test_case_task
        execute_test_case_task = get_execute_test_case_task()
        task = execute_test_case_task.delay(execucao.id, caso_id, user.id)
        execucao.rpa_id = task.id
        db.session.commit()
    except Exception as e:
        execucao.status = 'erro'
        execucao.fim = datetime.utcnow()
        db.session.commit()
        return response_error(f'Erro ao iniciar execução: {str(e)}', 500)

    return response_success(serialize_execucao(execucao), 'Execução iniciada com sucesso', 201)


@execucoes_bp.route('/<int:execucao_id>/logs', methods=['GET'])
@jwt_required()
def get_execution_logs(current_user_id, execucao_id):
    """Get logs for a specific execution."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    execucao = Execucao.query.get(execucao_id)
    if not execucao:
        return response_error('Execução não encontrada', 404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    level = request.args.get('level', type=str)  # Filter by log level: INFO, ERROR, WARNING
    
    query = Log.query.filter_by(execucao_id=execucao_id)
    
    if level:
        query = query.filter_by(nivel=level)
    
    query = query.order_by(Log.id.asc())
    paginated = query.paginate(page=max(1, page), per_page=min(200, max(1, per_page)), error_out=False)
    
    logs = []
    for log in paginated.items:
        logs.append({
            'id': log.id,
            'nivel': log.nivel,
            'mensagem': log.mensagem,
            'timestamp': log.timestamp.isoformat() if log.timestamp else None,
        })

    return response_success({
        'items': logs,
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'per_page': per_page,
    })


@execucoes_bp.route('/<int:execucao_id>/evidencias', methods=['GET'])
@jwt_required()
def get_execution_evidencias(current_user_id, execucao_id):
    """Get evidences (screenshots, logs, data) for a specific execution."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    execucao = Execucao.query.get(execucao_id)
    if not execucao:
        return response_error('Execução não encontrada', 404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    tipo = request.args.get('tipo', type=str)  # Filter by type: screenshot, log, data
    
    query = Evidencia.query.filter_by(execucao_id=execucao_id)
    
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    query = query.order_by(Evidencia.id.asc())
    paginated = query.paginate(page=max(1, page), per_page=min(200, max(1, per_page)), error_out=False)
    
    evidencias = []
    for evidencia in paginated.items:
        evidencias.append({
            'id': evidencia.id,
            'tipo': evidencia.tipo,
            'arquivo': evidencia.arquivo,
            'created_at': evidencia.created_at.isoformat() if evidencia.created_at else None,
        })

    return response_success({
        'items': evidencias,
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'per_page': per_page,
    })


@execucoes_bp.route('/<int:execucao_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_execution(current_user_id, execucao_id):
    """Cancel an ongoing execution."""
    user = User.query.get(current_user_id)
    if not user:
        return response_error('Usuário não encontrado', 404)

    execucao = Execucao.query.get(execucao_id)
    if not execucao:
        return response_error('Execução não encontrada', 404)

    if execucao.status in ['completada', 'erro', 'cancelada']:
        return response_error('Execução não pode ser cancelada (já concluída)', 400)

    # Revoke Celery task if it's running
    if execucao.rpa_id:
        try:
            from app.celery_app import celery
            celery.control.revoke(execucao.rpa_id, terminate=True)
        except Exception as e:
            pass  # Task already completed or not found

    execucao.status = 'cancelada'
    execucao.fim = datetime.utcnow()
    db.session.commit()

    return response_success(serialize_execucao(execucao), 'Execução cancelada com sucesso')
