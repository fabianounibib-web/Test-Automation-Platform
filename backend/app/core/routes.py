from flask import Blueprint, jsonify
from sqlalchemy import func
from app import db
from app.database.models import CasoTeste, Execucao, Log, Robo

core_bp = Blueprint('core', __name__)


@core_bp.route('/dashboard', methods=['GET'])
def dashboard():
    total_testes = CasoTeste.query.count()
    total_robos = Robo.query.count()
    execucoes = Execucao.query.order_by(Execucao.created_at.desc()).limit(5).all()
    tempo_medio = db.session.query(func.avg(Execucao.tempo)).scalar() or 0
    fila_execucao = Execucao.query.filter(Execucao.status == 'running').count()
    ultimos_erros = Log.query.filter(Log.nivel == 'error').order_by(Log.timestamp.desc()).limit(5).all()

    return jsonify({
        'total_testes': total_testes,
        'total_robos': total_robos,
        'ultimas_execucoes': [
            {
                'id': execucao.id,
                'status': execucao.status,
                'tempo': execucao.tempo
            }
            for execucao in execucoes
        ],
        'ultimos_erros': [
            {'id': log.id, 'mensagem': log.mensagem}
            for log in ultimos_erros
        ],
        'tempo_medio': round(float(tempo_medio), 2),
        'fila_execucao': fila_execucao
    }), 200
