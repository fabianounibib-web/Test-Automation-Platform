from flask import Blueprint, jsonify
from app.database.models import Execucao

execucoes_bp = Blueprint('execucoes', __name__)


@execucoes_bp.route('', methods=['GET'])
def get_execucoes():
    execucoes = Execucao.query.order_by(Execucao.id.desc()).all()
    return jsonify([
        {
            'id': execucao.id,
            'caso_teste_id': execucao.caso_teste_id,
            'status': execucao.status,
            'tempo': execucao.tempo,
            'created_at': execucao.created_at.isoformat() if execucao.created_at else None
        }
        for execucao in execucoes
    ]), 200


@execucoes_bp.route('/<int:id>', methods=['GET'])
def get_execucao(id):
    execucao = Execucao.query.get_or_404(id)
    return jsonify({
        'id': execucao.id,
        'caso_teste_id': execucao.caso_teste_id,
        'status': execucao.status,
        'tempo': execucao.tempo,
        'created_at': execucao.created_at.isoformat() if execucao.created_at else None
    }), 200
