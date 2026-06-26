from datetime import datetime
from app.celery_app import celery
from app import db
from app.database.models import Execucao, CasoTeste, Log, Evidencia
from app.core.rpa_client import execute_case as rpa_execute


@celery.task(name='execute_case_task')
def execute_case_task(caso_id):
    caso = CasoTeste.query.get(caso_id)
    if not caso:
        return {'error': 'caso not found'}

    caso.status = 'running'
    db.session.add(caso)

    execucao = Execucao(caso_teste_id=caso.id, inicio=datetime.utcnow(), status='running')
    db.session.add(execucao)
    db.session.commit()

    try:
        result = rpa_execute(caso, execucao.id)
        success = result.get('success', False)
        execucao.status = 'success' if success else 'failed'
        caso.status = 'executado com sucesso' if success else 'executado com erro'
        execucao.fim = datetime.utcnow()
        execucao.tempo = (execucao.fim - execucao.inicio).total_seconds()
        db.session.commit()

        for l in result.get('logs', []):
            db.session.add(Log(execucao_id=execucao.id, nivel=l.get('nivel', 'info'), mensagem=l.get('mensagem', '')))

        for e in result.get('evidencias', []):
            db.session.add(Evidencia(execucao_id=execucao.id, arquivo=e.get('arquivo'), tipo=e.get('tipo')))

        if not result.get('logs'):
            db.session.add(Log(execucao_id=execucao.id, nivel='info', mensagem='Execução finalizada sem logs adicionais.'))

        db.session.commit()
    except Exception as exc:
        execucao.status = 'error'
        caso.status = 'executado com erro'
        execucao.fim = datetime.utcnow()
        execucao.tempo = (execucao.fim - execucao.inicio).total_seconds()
        db.session.commit()
        db.session.add(Log(execucao_id=execucao.id, nivel='error', mensagem=str(exc)))
        db.session.commit()

    return {'execucao_id': execucao.id, 'status': execucao.status}
