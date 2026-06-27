from abc import ABC, abstractmethod


class BaseExecutor(ABC):
    name = 'base'

    @abstractmethod
    def execute(self, robo, execucao_id):
        raise NotImplementedError


class PythonExecutor(BaseExecutor):
    name = 'python'

    def execute(self, robo, execucao_id):
        return {
            'success': True,
            'executor': self.name,
            'execucao_id': execucao_id,
            'message': f"Executor {self.name} recebeu a automação '{robo.nome}'."
        }


class PlaywrightExecutor(BaseExecutor):
    name = 'playwright'

    def execute(self, robo, execucao_id):
        return {
            'success': True,
            'executor': self.name,
            'execucao_id': execucao_id,
            'message': f"Executor {self.name} recebeu a automação '{robo.nome}'."
        }


class SeleniumExecutor(BaseExecutor):
    name = 'selenium'

    def execute(self, robo, execucao_id):
        return {
            'success': True,
            'executor': self.name,
            'execucao_id': execucao_id,
            'message': f"Executor {self.name} recebeu a automação '{robo.nome}'."
        }


class ExecutorRegistry:
    def __init__(self):
        self._executors = {}

    def register(self, executor):
        self._executors[executor.name] = executor
        return executor

    def get(self, name):
        return self._executors.get(name)

    def available(self):
        return sorted(self._executors.keys())


executor_registry = ExecutorRegistry()
executor_registry.register(PythonExecutor())
executor_registry.register(PlaywrightExecutor())
executor_registry.register(SeleniumExecutor())


def dispatch_executor(robo, execucao_id):
    executor = executor_registry.get((robo.tipo or 'python').strip().lower())
    if executor is None:
        executor = executor_registry.get('python')
    return executor.execute(robo, execucao_id)
