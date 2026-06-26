from flask import Blueprint, request, jsonify
from app.tasks.execute_case import execute_case_task

testes_bp = Blueprint('testes', __name__)


@testes_bp.route('', methods=['GET'])
def get_casos():
    return jsonify([]), 200


@testes_bp.route('/<int:id>/executar', methods=['POST'])
def executar_caso(id):
    # enqueue task via Celery
    task = execute_case_task.delay(id)
    return jsonify({'task_id': task.id}), 202
