"""
Celery based task
"""
from metadash import app
from celery import Celery, current_task


def make_celery(app):
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


celery = make_celery(app)


def debounce_wrapper(fn):
    # TODO
    pass


def update_task_info(summary, meta=None):
    """
    If running as task, update the task summary, else return directly
    """
    if current_task.request.id is not None:
        current_task.update_state(
            state=(summary[:35] + '..' + summary[-10:]) if len(summary) > 49 else summary,
            meta=meta)


def task(*args, **kwargs):
    """
    Task wrapper
    """
    debounce = kwargs.get('debounce', None)
    if debounce:
        raise NotImplementedError()
    return celery.task(*args, **kwargs)
