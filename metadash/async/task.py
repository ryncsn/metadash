"""
Celery based task
"""
import logging

from celery import current_task
from .celery import celery

logger = logging.getLogger(__name__)

cron = []


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
    Simple task wrapper
    """
    debounce = kwargs.get('debounce', None)
    periodic = kwargs.get('periodic', None)
    if debounce:
        raise NotImplementedError()

    def task_wrapper(fn):
        """
        wrap again before return so we can catch the task
        """
        task = celery.task(*args, **kwargs)(fn)
        if periodic:
            assert isinstance(periodic, int)
            cron.append((periodic, task))
        return task

    return task_wrapper


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    for periodic, task in cron:
        sender.add_periodic_task(10.0, task.s(), name="Periodic Task")
