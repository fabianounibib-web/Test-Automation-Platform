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
    for key, replacement in runtime_values.items():
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


def execute_connector_flow(conector, execucao_id, runtime_values=None):
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
    for index, step in enumerate(steps, start=1):
        logs.append({
            'nivel': 'info',
            'mensagem': f"Passo {index}: {describe_step(step, runtime_values)}."
        })

    return {
        'success': True,
        'execucao_id': execucao_id,
        'message': f"Conector '{conector.nome}' interpretado com sucesso.",
        'steps_executed': len(steps),
        'logs': logs,
    }
