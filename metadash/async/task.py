"""
Celery based task
"""
import logging

from celery import current_task
from .celery import celery

logger = logging.getLogger(__name__)

cron = []


class DummyTask(object):
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        self.fn(*args, **kwargs)

    def apply_async(self, args=None, kwargs=None, **options):
        args = args or ()
        kwargs = kwargs or {}
        logger.warning("Running async tasks in main thread, this will block main server"
                       "and slow down the performance, and options will be ignored")
        self.fn(*args, **kwargs)
        return self  # TODO: mimic celey task return

    def delay(self, *args, **kwargs):
        self.fn(*args, **kwargs)
        return self  # TODO: mimic celey task return


def debounce_wrapper(fn):
    # TODO
    pass


def update_task_info(summary, meta=None):
    """
    If running as task, update the task summary, else return directly
    """
    if current_task and current_task.request.id is not None:
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

    def dumb_wrapper(fn):
        return DummyTask(fn)

    def task_wrapper(fn):
        """
        wrap again before return so we can catch the task
        """
        task = celery.task(*args, **kwargs)(fn)
        if periodic:
            assert isinstance(periodic, int)
            cron.append((periodic, task))
        return task

    if celery:
        return task_wrapper
    else:
        return dumb_wrapper


if celery is not None:
    @celery.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        for periodic, task in cron:
            sender.add_periodic_task(60.0, task.s(), name="Periodic Task")
