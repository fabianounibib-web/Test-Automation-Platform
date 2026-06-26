from flask import Blueprint, jsonify

core_bp = Blueprint('core', __name__)


@core_bp.route('/dashboard', methods=['GET'])
def dashboard():
    # placeholder metrics
    return jsonify({
        'total_testes': 0,
        'ultimas_execucoes': [],
        'ultimos_erros': [],
        'tempo_medio': 0,
        'fila_execucao': 0
    }), 200
