"""
Celery based task
"""
import logging

from metadash import app
from celery import Celery

logger = logging.getLogger(__name__)


def make_celery(app):
    if app.config['CELERY_RESULT_BACKEND'] and app.config['CELERY_BROKER_URL']:
        celery = Celery(app.import_name,
                        backend=app.config['CELERY_RESULT_BACKEND'],
                        broker=app.config['CELERY_BROKER_URL'])
        celery.conf.update(app.config)
        TaskBase = celery.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask
        return celery
    else:
        logger.error("Celery disable, redis backend is required.")
        return None


celery = make_celery(app)
