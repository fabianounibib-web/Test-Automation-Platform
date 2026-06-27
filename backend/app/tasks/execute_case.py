from datetime import datetime
from flask import current_app
from celery import Celery
from app import db
from app.core.connectors import execute_connector_flow
from app.database.models import Execucao, CasoTeste, Log, Evidencia, Conector


# Lazy import to avoid circular imports
def get_celery():
    """Get celery instance lazily using the current Flask app config."""
    try:
        app = current_app._get_current_object()
        broker_url = app.config.get('CELERY_BROKER_URL') or app.config.get('REDIS_URL')
        backend_url = app.config.get('CELERY_RESULT_BACKEND') or app.config.get('REDIS_URL')

        celery = Celery(
            app.import_name,
            broker=broker_url,
            backend=backend_url,
        )
        celery_conf = {
            key[len('CELERY_'):].lower(): value
            for key, value in app.config.items()
            if key.startswith('CELERY_')
        }
        celery.conf.update(celery_conf)
        celery.conf.task_always_eager = app.config.get('CELERY_TASK_ALWAYS_EAGER', False)
        celery.conf.task_eager_propagates = app.config.get('CELERY_TASK_EAGER_PROPAGATES', False)

        TaskBase = celery.Task

        class ContextTask(TaskBase):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask
        return celery
    except RuntimeError:
        from app.celery_app import celery
        return celery


execute_test_case_task = None


def _create_execute_task():
    """Factory to create the Celery task."""
    celery = get_celery()
    
    @celery.task(name='execute_test_case', bind=True, max_retries=3)
    def execute_test_case(self, execucao_id, caso_id, user_id):
        """Execute a test case via RPA."""
        try:
            execucao = Execucao.query.get(execucao_id)
            if not execucao:
                return {'error': 'Execução não encontrada', 'status': 'erro'}

            caso = CasoTeste.query.get(caso_id)
            if not caso:
                return {'error': 'Caso de teste não encontrado', 'status': 'erro'}

            # Update execution status to running
            execucao.status = 'executando'
            execucao.inicio = datetime.utcnow()
            db.session.commit()

            # Log: execution started
            log_entry = Log(
                execucao_id=execucao_id,
                nivel='INFO',
                mensagem=f'Execução iniciada para caso: {caso.nome}'
            )
            db.session.add(log_entry)
            db.session.commit()

            # Load connector for the case
            conector = None
            if caso.conector_id:
                conector = Conector.query.get(caso.conector_id)

            if not conector:
                execucao.status = 'erro'
                execucao.fim = datetime.utcnow()
                execucao.tempo = (execucao.fim - execucao.inicio).total_seconds()
                log_entry = Log(
                    execucao_id=execucao_id,
                    nivel='ERROR',
                    mensagem='Caso não possui conector associado para execução.'
                )
                db.session.add(log_entry)
                db.session.commit()
                return {
                    'execucao_id': execucao_id,
                    'status': execucao.status,
                    'classificacao': 'erro',
                    'tempo': execucao.tempo
                }

            # Execute connector flow using runtime data from the case
            result = execute_connector_flow(
                conector,
                execucao_id,
                runtime_values=caso.dados or {},
                evidence_dir=current_app.config.get('EVIDENCIAS_FOLDER'),
            )

            # Persist logs from connector execution
            for item in result.get('logs', []):
                db.session.add(Log(
                    execucao_id=execucao_id,
                    nivel=item.get('nivel', 'INFO').upper(),
                    mensagem=item.get('mensagem', '')
                ))

            # Persist evidence if available
            evidence_path = result.get('evidence_path')
            if evidence_path:
                db.session.add(Evidencia(
                    execucao_id=execucao_id,
                    arquivo=evidence_path,
                    tipo='report'
                ))

            if not result.get('success', False):
                execucao.status = 'erro'
                classificacao = 'erro'
            else:
                execucao.status = 'sucesso'
                classificacao = 'sucesso'

            execucao.fim = datetime.utcnow()
            execucao.tempo = (execucao.fim - execucao.inicio).total_seconds()
            execucao.rpa_id = str(self.request.id or self.request.id)
            db.session.commit()

            return {
                'execucao_id': execucao_id,
                'status': execucao.status,
                'classificacao': classificacao,
                'tempo': execucao.tempo
            }

        except Exception as exc:
            try:
                execucao = Execucao.query.get(execucao_id)
                if execucao:
                    execucao.status = 'erro'
                    execucao.fim = datetime.utcnow()
                    if execucao.inicio:
                        execucao.tempo = (execucao.fim - execucao.inicio).total_seconds()
                    
                    log_entry = Log(
                        execucao_id=execucao_id,
                        nivel='ERROR',
                        mensagem=f'Erro durante execução: {str(exc)}'
                    )
                    db.session.add(log_entry)
                    db.session.commit()
            except Exception as db_err:
                print(f'Erro ao salvar erro da execução: {db_err}')

            # Retry with exponential backoff
            return self.retry(exc=exc, countdown=2 ** self.request.retries)

    return execute_test_case


# Create the Celery task lazily
def get_execute_test_case_task():
    """Get the execute_test_case task (lazy loaded)."""
    global execute_test_case_task
    if execute_test_case_task is None:
        execute_test_case_task = _create_execute_task()
    return execute_test_case_task
