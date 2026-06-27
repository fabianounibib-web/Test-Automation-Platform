from celery import Celery
from app import create_app
from app.config import Config

flask_app = create_app(Config)

broker_url = flask_app.config.get('CELERY_BROKER_URL') or flask_app.config.get('REDIS_URL')
backend_url = flask_app.config.get('CELERY_RESULT_BACKEND') or flask_app.config.get('REDIS_URL')

celery = Celery(
    flask_app.import_name,
    broker=broker_url,
    backend=backend_url
)

celery_conf = {
    key[len('CELERY_'):].lower(): value
    for key, value in flask_app.config.items()
    if key.startswith('CELERY_')
}
celery.conf.update(celery_conf)

# Ensure Celery honors eager settings from Flask config
if 'CELERY_TASK_ALWAYS_EAGER' in flask_app.config:
    celery.conf.task_always_eager = flask_app.config['CELERY_TASK_ALWAYS_EAGER']
if 'CELERY_TASK_EAGER_PROPAGATES' in flask_app.config:
    celery.conf.task_eager_propagates = flask_app.config['CELERY_TASK_EAGER_PROPAGATES']

TaskBase = celery.Task


class ContextTask(TaskBase):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)


celery.Task = ContextTask
