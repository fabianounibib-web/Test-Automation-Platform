from celery import Celery
from app import create_app
from app.config import Config

flask_app = create_app(Config)

celery = Celery(
    flask_app.import_name,
    broker=flask_app.config.get('REDIS_URL'),
    backend=flask_app.config.get('REDIS_URL')
)

celery.conf.update(flask_app.config)

TaskBase = celery.Task


class ContextTask(TaskBase):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)


celery.Task = ContextTask
