from datetime import datetime

from flask import Blueprint, jsonify, request

from app import db
from app.database.models import Execucao, Log, Robo
from app.core.executors import dispatch_executor

robos_bp = Blueprint('robos', __name__)


@robos_bp.route('', methods=['GET'])
def get_robos():
    robos = Robo.query.order_by(Robo.id.desc()).all()
    return jsonify([
        {
            'id': robo.id,
            'nome': robo.nome,
            'descricao': robo.descricao,
            'tipo': robo.tipo,
            'status': robo.status,
            'created_at': robo.created_at.isoformat() if robo.created_at else None
        }
        for robo in robos
    ]), 200


@robos_bp.route('', methods=['POST'])
def create_robo():
    payload = request.get_json(silent=True) or {}
    nome = (payload.get('nome') or '').strip()
    if not nome:
        return jsonify({'error': 'nome é obrigatório'}), 400

    robo = Robo(
        nome=nome,
        descricao=(payload.get('descricao') or '').strip(),
        tipo=(payload.get('tipo') or 'python').strip(),
        script=(payload.get('script') or '').strip(),
        status=(payload.get('status') or 'draft').strip()
    )
    db.session.add(robo)
    db.session.commit()

    return jsonify({
        'id': robo.id,
        'nome': robo.nome,
        'descricao': robo.descricao,
        'tipo': robo.tipo,
        'status': robo.status,
        'created_at': robo.created_at.isoformat() if robo.created_at else None
    }), 201


@robos_bp.route('/<int:id>', methods=['GET'])
def get_robo(id):
    robo = Robo.query.get_or_404(id)
    return jsonify({
        'id': robo.id,
        'nome': robo.nome,
        'descricao': robo.descricao,
        'tipo': robo.tipo,
        'script': robo.script,
        'status': robo.status,
        'created_at': robo.created_at.isoformat() if robo.created_at else None
    }), 200


@robos_bp.route('/<int:id>/executar', methods=['POST'])
def executar_robo(id):
    robo = Robo.query.get_or_404(id)

    execucao = Execucao(
        robo_id=robo.id,
        inicio=datetime.utcnow(),
        status='running',
        rpa_id=str(robo.id)
    )
    db.session.add(execucao)
    db.session.commit()

    result = dispatch_executor(robo, execucao.id)
    execucao.status = 'success' if result.get('success') else 'failed'
    execucao.fim = datetime.utcnow()
    execucao.tempo = (execucao.fim - execucao.inicio).total_seconds()

    db.session.add(Log(
        execucao_id=execucao.id,
        nivel='info',
        mensagem=result.get('message', f"Orquestrador recebeu a automação '{robo.nome}' para execução.")
    ))
    db.session.commit()

    return jsonify({
        'id': execucao.id,
        'robo_id': robo.id,
        'status': execucao.status,
        'tempo': execucao.tempo,
        'executor': result.get('executor', 'python'),
        'message': result.get('message', 'Automação registrada pelo orquestrador web.')
    }), 202
