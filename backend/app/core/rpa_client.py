import requests
from flask import current_app


def execute_case(caso, execucao_id):
    url = current_app.config.get('RPA_API_URL', 'http://rpa:8000/execute')
    payload = {
        'caso_id': caso.id,
        'dados': caso.dados or {},
        'execucao_id': execucao_id,
    }
    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {'success': False, 'error': str(e)}
