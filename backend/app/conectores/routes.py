from datetime import datetime

from flask import Blueprint, jsonify, request

from app import db
from app.core.connectors import execute_connector_flow, validate_steps
from app.database.models import Conector, Execucao, Log

conectores_bp = Blueprint('conectores', __name__)


def serialize_conector(conector, include_steps=True):
    payload = {
        'id': conector.id,
        'nome': conector.nome,
        'descricao': conector.descricao,
        'url_base': conector.url_base,
        'ambiente': conector.ambiente,
        'status': conector.status,
        'versao': conector.versao,
        'credenciais_ref': conector.credenciais_ref,
        'created_at': conector.created_at.isoformat() if conector.created_at else None,
        'updated_at': conector.updated_at.isoformat() if conector.updated_at else None,
    }
    if include_steps:
        payload['steps'] = conector.steps or []
    return payload


@conectores_bp.route('', methods=['GET'])
def get_conectores():
    conectores = Conector.query.order_by(Conector.id.desc()).all()
    return jsonify([serialize_conector(conector, include_steps=False) for conector in conectores]), 200


@conectores_bp.route('', methods=['POST'])
def create_conector():
    payload = request.get_json(silent=True) or {}
    nome = (payload.get('nome') or '').strip()
    url_base = (payload.get('url_base') or '').strip()
    steps = payload.get('steps') or []

    if not nome:
        return jsonify({'error': 'nome é obrigatório'}), 400
    if not url_base:
        return jsonify({'error': 'url_base é obrigatória'}), 400

    errors = validate_steps(steps)
    if errors:
        return jsonify({'error': 'fluxo inválido', 'details': errors}), 400

    conector = Conector(
        nome=nome,
        descricao=(payload.get('descricao') or '').strip(),
        url_base=url_base,
        ambiente=(payload.get('ambiente') or 'produção').strip(),
        status=(payload.get('status') or 'draft').strip(),
        versao=(payload.get('versao') or '1.0.0').strip(),
        credenciais_ref=payload.get('credenciais_ref') or {},
        steps=steps,
    )
    db.session.add(conector)
    db.session.commit()

    return jsonify(serialize_conector(conector)), 201


@conectores_bp.route('/<int:id>', methods=['GET'])
def get_conector(id):
    conector = Conector.query.get_or_404(id)
    return jsonify(serialize_conector(conector)), 200


@conectores_bp.route('/<int:id>/executar', methods=['POST'])
def executar_conector(id):
    conector = Conector.query.get_or_404(id)
    payload = request.get_json(silent=True) or {}

    execucao = Execucao(
        inicio=datetime.utcnow(),
        status='running',
        rpa_id=f'conector:{conector.id}'
    )
    db.session.add(execucao)
    db.session.commit()

    result = execute_connector_flow(conector, execucao.id, runtime_values=payload.get('variaveis') or {})
    execucao.status = 'success' if result.get('success') else 'failed'
    execucao.fim = datetime.utcnow()
    execucao.tempo = (execucao.fim - execucao.inicio).total_seconds()

    for entry in result.get('logs', []):
        db.session.add(Log(
            execucao_id=execucao.id,
            nivel=entry.get('nivel', 'info'),
            mensagem=entry.get('mensagem', '')
        ))

    db.session.commit()

    return jsonify({
        'id': execucao.id,
        'conector_id': conector.id,
        'status': execucao.status,
        'tempo': execucao.tempo,
        'message': result.get('message'),
        'steps_executed': result.get('steps_executed', 0),
    }), 202
