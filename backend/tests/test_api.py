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
            'REDIS_URL': 'redis://localhost:6379/0',
            'RPA_API_URL': 'http://localhost:8000/execute',
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


if __name__ == '__main__':
    unittest.main()
