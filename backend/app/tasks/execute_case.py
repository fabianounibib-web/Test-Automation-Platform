from datetime import datetime
from app import db
from app.database.models import Execucao, CasoTeste, Log


# Lazy import to avoid circular imports
def get_celery():
    """Get celery instance lazily."""
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

            # TODO: Implement actual RPA execution here
            # For MVP, this will be a placeholder that simulates execution
            # Later, this will integrate with Playwright or other RPA engines

            # Simulate execution
            resultado_obtido = 'Teste executado com sucesso'
            resultado_esperado = caso.resultado_esperado or 'Execução concluída sem erros'

            # Compare result with expected (simplified)
            if 'sucesso' in resultado_obtido.lower() and 'erro' not in resultado_obtido.lower():
                execucao.status = 'sucesso'
                classificacao = 'sucesso'
            else:
                execucao.status = 'erro'
                classificacao = 'erro_funcional'

            # Calculate execution time
            execucao.fim = datetime.utcnow()
            execucao.tempo = (execucao.fim - execucao.inicio).total_seconds()

            # Log: execution completed
            log_entry = Log(
                execucao_id=execucao_id,
                nivel='INFO',
                mensagem=f'Execução concluída. Resultado: {classificacao}. Tempo: {execucao.tempo:.2f}s'
            )
            db.session.add(log_entry)
            db.session.commit()

            # Update execution record
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
