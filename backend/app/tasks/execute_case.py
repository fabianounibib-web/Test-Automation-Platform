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

    execucao = Execucao(caso_teste_id=caso.id, inicio=datetime.utcnow(), status='running')
    db.session.add(execucao)
    db.session.commit()

    try:
        result = rpa_execute(caso, execucao.id)
        # result expected: {'success': bool, 'logs': [...], 'evidencias': [...]}
        success = result.get('success', False)
        execucao.status = 'success' if success else 'failed'
        execucao.fim = datetime.utcnow()
        execucao.tempo = (execucao.fim - execucao.inicio).total_seconds()
        db.session.commit()

        for l in result.get('logs', []):
            log = Log(execucao_id=execucao.id, nivel=l.get('nivel', 'info'), mensagem=l.get('mensagem', ''))
            db.session.add(log)

        for e in result.get('evidencias', []):
            ev = Evidencia(execucao_id=execucao.id, arquivo=e.get('arquivo'), tipo=e.get('tipo'))
            db.session.add(ev)

        db.session.commit()
    except Exception as exc:
        execucao.status = 'error'
        execucao.fim = datetime.utcnow()
        execucao.tempo = (execucao.fim - execucao.inicio).total_seconds()
        db.session.commit()
        log = Log(execucao_id=execucao.id, nivel='error', mensagem=str(exc))
        db.session.add(log)
        db.session.commit()

    return {'execucao_id': execucao.id, 'status': execucao.status}
