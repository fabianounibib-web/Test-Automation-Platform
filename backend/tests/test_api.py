import unittest

from app import create_app, db
from app.config import Config


class ApiEndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(type('TestConfig', (), {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SECRET_KEY': 'test-secret',
            'JWT_SECRET_KEY': 'test-jwt',
            'UPLOAD_FOLDER': '/tmp',
            'EVIDENCIAS_FOLDER': '/tmp',
            'LOGS_FOLDER': '/tmp',
            'REDIS_URL': 'memory://',
            'CELERY_BROKER_URL': 'memory://',
            'CELERY_RESULT_BACKEND': 'cache+memory://',
            'RPA_API_URL': 'http://localhost:8000/execute',
            'CELERY_TASK_ALWAYS_EAGER': True,
            'CELERY_TASK_EAGER_PROPAGATES': True,
        }))
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_cliente_and_dashboard(self):
        response = self.client.post('/api/clientes', json={
            'nome': 'Cliente Teste',
            'email': 'cliente@teste.com',
            'responsavel': 'Ana'
        })
        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload['nome'], 'Cliente Teste')

        dashboard = self.client.get('/api/dashboard')
        self.assertEqual(dashboard.status_code, 200)
        self.assertIn('total_testes', dashboard.get_json())

    def test_create_robo_and_list(self):
        response = self.client.post('/api/robos', json={
            'nome': 'RPA Login',
            'descricao': 'Automação de login para o portal',
            'tipo': 'python',
            'script': 'print("ok")',
            'status': 'draft'
        })
        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload['nome'], 'RPA Login')

        list_response = self.client.get('/api/robos')
        self.assertEqual(list_response.status_code, 200)
        self.assertTrue(any(item['nome'] == 'RPA Login' for item in list_response.get_json()))

    def test_execute_robo_uses_executor_dispatcher(self):
        create_response = self.client.post('/api/robos', json={
            'nome': 'Robo Python',
            'descricao': 'Execução via executor python',
            'tipo': 'python',
            'script': 'print("ok")',
            'status': 'ready'
        })
        self.assertEqual(create_response.status_code, 201)
        robo_id = create_response.get_json()['id']

        execute_response = self.client.post(f'/api/robos/{robo_id}/executar')
        self.assertEqual(execute_response.status_code, 202)
        payload = execute_response.get_json()
        self.assertEqual(payload['status'], 'success')
        self.assertEqual(payload['executor'], 'python')

    def test_create_and_execute_conector(self):
        response = self.client.post('/api/conectores', json={
            'nome': 'Portal XPTO',
            'descricao': 'Baixa histórico de pagamentos',
            'url_base': 'https://xpto.com',
            'credenciais_ref': {
                'usuario': 'vault://cliente/xpto/usuario',
                'senha': 'vault://cliente/xpto/senha'
            },
            'steps': [
                {'action': 'goto', 'url': 'https://xpto.com'},
                {'action': 'fill', 'target': 'usuario', 'selector': '#usuario', 'value': '${usuario}'},
                {'action': 'fill', 'target': 'senha', 'selector': '#senha', 'value': '${senha}'},
                {'action': 'click', 'target': 'entrar', 'selector': '#entrar'},
                {'action': 'download', 'target': 'historico_pagamentos', 'selector': '#download'}
            ]
        })
        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload['nome'], 'Portal XPTO')
        self.assertEqual(len(payload['steps']), 5)

        list_response = self.client.get('/api/conectores')
        self.assertEqual(list_response.status_code, 200)
        self.assertTrue(any(item['nome'] == 'Portal XPTO' for item in list_response.get_json().get('items', [])))

        execute_response = self.client.post(f'/api/conectores/{payload["id"]}/executar', json={
            'variaveis': {
                'usuario': 'ana',
                'senha': 'segredo'
            }
        })
        self.assertEqual(execute_response.status_code, 202)
        execute_payload = execute_response.get_json()
        self.assertEqual(execute_payload['status'], 'success')
        self.assertEqual(execute_payload['steps_executed'], 5)

    def test_reject_invalid_conector_flow(self):
        response = self.client.post('/api/conectores', json={
            'nome': 'Portal inválido',
            'url_base': 'https://xpto.com',
            'steps': [{'action': 'fill'}]
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('details', response.get_json())

    def test_execute_caso_with_conector(self):
        # Create connector with a simple flow
        connector_response = self.client.post('/api/conectores', json={
            'nome': 'Portal XPTO',
            'descricao': 'Baixa histórico de pagamentos',
            'url_base': 'https://xpto.com',
            'credenciais_ref': {
                'usuario': 'vault://cliente/xpto/usuario',
                'senha': 'vault://cliente/xpto/senha'
            },
            'steps': [
                {'action': 'goto', 'url': 'https://xpto.com'},
                {'action': 'fill', 'target': 'usuario', 'selector': '#usuario', 'value': '${usuario}'},
                {'action': 'fill', 'target': 'senha', 'selector': '#senha', 'value': '${senha}'},
                {'action': 'click', 'target': 'entrar', 'selector': '#entrar'},
                {'action': 'download', 'target': 'historico_pagamentos', 'selector': '#download'}
            ]
        })
        self.assertEqual(connector_response.status_code, 201)
        connector_id = connector_response.get_json()['id']

        caso_response = self.client.post('/api/casos', json={
            'nome': 'Caso com conector',
            'objetivo': 'Executar portal',
            'conector_id': connector_id,
            'dados': {
                'usuario': 'ana',
                'senha': 'segredo'
            }
        })
        self.assertEqual(caso_response.status_code, 201)
        caso_id = caso_response.get_json()['id']

        execute_response = self.client.post(f'/api/execucoes/casos/{caso_id}/execute')
        self.assertEqual(execute_response.status_code, 201)
        payload = execute_response.get_json()
        self.assertEqual(payload['status'], 'sucesso')
        self.assertIn('rpa_id', payload)
        self.assertEqual(payload['caso_teste_id'], caso_id)

        # Verify execution record was persisted
        execution_id = payload['id']
        exec_detail = self.client.get(f'/api/execucoes/{execution_id}')
        self.assertEqual(exec_detail.status_code, 200)
        self.assertEqual(exec_detail.get_json().get('status'), 'sucesso')


if __name__ == '__main__':
    unittest.main()
