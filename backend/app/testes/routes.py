from flask import Blueprint, jsonify
from app import db
from app.database.models import CasoTeste
from app.tasks.execute_case import execute_case_task

testes_bp = Blueprint('testes', __name__)


@testes_bp.route('', methods=['GET'])
def get_casos():
    casos = CasoTeste.query.order_by(CasoTeste.id.desc()).all()
    return jsonify([
        {
            'id': caso.id,
            'roteiro_id': caso.roteiro_id,
            'nome': caso.nome,
            'objetivo': caso.objetivo,
            'status': caso.status
        }
        for caso in casos
    ]), 200


@testes_bp.route('/<int:id>/executar', methods=['POST'])
def executar_caso(id):
    caso = CasoTeste.query.get(id)
    if not caso:
        return jsonify({'error': 'caso não encontrado'}), 404

    task = execute_case_task.delay(id)
    return jsonify({'task_id': task.id, 'status': 'queued'}), 202
