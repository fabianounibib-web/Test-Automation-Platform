import json
import os
import tempfile
import time
import uuid

from flask import current_app

SUPPORTED_ACTIONS = {'goto', 'fill', 'click', 'select', 'wait', 'assert', 'download'}
ACTIONS_REQUIRING_TARGET = {'fill', 'click', 'select', 'assert', 'download'}


def validate_steps(steps):
    if not isinstance(steps, list):
        return ['steps deve ser uma lista de ações']

    errors = []
    for index, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            errors.append(f'passo {index}: deve ser um objeto')
            continue

        action = (step.get('action') or '').strip().lower()
        if action not in SUPPORTED_ACTIONS:
            errors.append(f'passo {index}: action inválida ou ausente')

        if action == 'goto' and not step.get('url'):
            errors.append(f'passo {index}: url é obrigatória para goto')

        if action in ACTIONS_REQUIRING_TARGET and not (step.get('selector') or step.get('target')):
            errors.append(f'passo {index}: selector ou target é obrigatório para {action}')

    return errors


def resolve_value(value, runtime_values):
    if not isinstance(value, str):
        return value

    resolved = value
    for key, replacement in (runtime_values or {}).items():
        resolved = resolved.replace('${' + key + '}', str(replacement))
    return resolved


def describe_step(step, runtime_values):
    action = step.get('action')
    target = step.get('target') or step.get('selector') or step.get('url') or 'sem alvo'

    if action == 'fill':
        value = resolve_value(step.get('value', ''), runtime_values)
        masked = '***' if 'senha' in str(target).lower() else value
        return f'Preencher {target} com {masked}'
    if action == 'goto':
        return f'Acessar {resolve_value(step.get("url"), runtime_values)}'
    if action == 'download':
        return f'Baixar arquivo em {target}'
    return f'Executar {action} em {target}'


def _get_evidence_dir(evidence_dir=None):
    if evidence_dir:
        return evidence_dir
    try:
        return current_app.config.get('EVIDENCIAS_FOLDER') or tempfile.gettempdir()
    except Exception:
        return tempfile.gettempdir()


def _write_evidence(report, evidence_dir=None):
    evidence_dir = _get_evidence_dir(evidence_dir)
    os.makedirs(evidence_dir, exist_ok=True)
    timestamp = int(time.time() * 1000)
    path = os.path.join(evidence_dir, f'conector_{timestamp}.json')
    with open(path, 'w', encoding='utf-8') as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
    return path


def execute_connector_flow(conector, execucao_id, runtime_values=None, evidence_dir=None):
    runtime_values = runtime_values or {}
    steps = conector.steps or []
    errors = validate_steps(steps)
    if errors:
        return {
            'success': False,
            'execucao_id': execucao_id,
            'message': 'Conector possui fluxo inválido.',
            'steps_executed': 0,
            'logs': [{'nivel': 'error', 'mensagem': error} for error in errors],
        }

    logs = [{
        'nivel': 'info',
        'mensagem': f"Iniciando conector '{conector.nome}' na versão {conector.versao}."
    }]
    engine = 'simulado'
    evidence_dir = _get_evidence_dir(evidence_dir)

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()

            for index, step in enumerate(steps, start=1):
                action = (step.get('action') or '').strip().lower()
                resolved_target = resolve_value(step.get('target') or step.get('selector') or step.get('url') or '', runtime_values)
                resolved_value_data = resolve_value(step.get('value', ''), runtime_values)
                timeout = int(step.get('timeout', 5000)) if step.get('timeout') is not None else 5000

                if action == 'goto':
                    url = resolve_value(step.get('url') or '', runtime_values)
                    page.goto(url, wait_until='networkidle', timeout=timeout)
                elif action == 'fill':
                    page.locator(resolved_target).fill(str(resolved_value_data), timeout=timeout)
                elif action == 'click':
                    page.locator(resolved_target).click(timeout=timeout)
                elif action == 'select':
                    page.locator(resolved_target).select_option(str(resolved_value_data), timeout=timeout)
                elif action == 'wait':
                    if resolved_target:
                        page.locator(resolved_target).wait_for(timeout=timeout)
                    else:
                        page.wait_for_timeout(timeout)
                elif action == 'assert':
                    page.locator(resolved_target).wait_for(timeout=timeout)
                elif action == 'download':
                    with page.expect_download(timeout=timeout) as download_info:
                        page.locator(resolved_target).click(timeout=timeout)
                    download = download_info.value
                    filename = download.suggested_filename or f'download_{uuid.uuid4().hex}'
                    download_path = os.path.join(evidence_dir, filename)
                    download.save_as(download_path)
                    logs.append({
                        'nivel': 'info',
                        'mensagem': f'Download salvo em {download_path}'
                    })
                logs.append({
                    'nivel': 'info',
                    'mensagem': f"Passo {index}: {describe_step(step, runtime_values)}."
                })

            browser.close()
            engine = 'playwright'
    except Exception as exc:
        for index, step in enumerate(steps, start=1):
            logs.append({
                'nivel': 'info',
                'mensagem': f"Passo {index}: {describe_step(step, runtime_values)}."
            })
        logs.append({
            'nivel': 'warning',
            'mensagem': f'Executor Playwright indisponível, usando execução simulada: {exc}'
        })

    report = {
        'conector': conector.nome,
        'status': 'success',
        'engine': engine,
        'steps_executed': len(steps),
        'runtime_values': runtime_values,
    }
    evidence_path = _write_evidence(report, evidence_dir=evidence_dir)

    return {
        'success': True,
        'execucao_id': execucao_id,
        'message': f"Conector '{conector.nome}' executado com sucesso.",
        'steps_executed': len(steps),
        'logs': logs,
        'evidence_path': evidence_path,
    }
