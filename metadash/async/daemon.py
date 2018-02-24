"""
Celery based task
"""
import uuid
import time
import logging
import itertools

from metadash.cache import get_mutex

from celery import Task
# from celery.signals import worker_shutting_down
from .task import task
from .inspect import get_running_task_status

logger = logging.getLogger(__name__)


Daemons = {
}


def current_milli_time():
    return round(time.time() * 1000)


class Daemon(Task):
    """
    Daemon Instance
    """

    def __init__(self, fn, heartbeat_interval=None, daemon_name=None):
        self.daemon_instance_id = str(uuid.uuid1())
        self.daemon_name = daemon_name
#        self.heartbeat_interval = heartbeat_interval or 10 * 1000  # 10 sec, 10000 msec
        self.task = task(bind=True, name=daemon_name)(fn)

#    def is_alive(self):
#        last_heartbeat = (get_(self.daemon_name) or {}).get(self.daemon_instance_id, {}).get("heartbeat")
#        if last_heartbeat and current_milli_time - last_heartbeat > self.heartbeat_interval:
#            return False
#        return True

    def run(self):
        if not self._exit_fn:
            logger.warn("Daemon %s don't have a exit handler, it may not shutdown gracefully", self.daemon_name)
        self.task.delay()

#    def heartbeat(self):
#        return get_or_create(self.daemon_name, lambda: {
#            "instance": self.daemon_instance_id,
#            "heartbeat": current_milli_time()
#        })


@task(periodic=10)
def guardian():
    """
    Guardian task
    """
    mutex = get_mutex('metadash_daemon_guardian')
    # Won't work if there is not mutex backend avaliable
    if mutex:
        with mutex:
            running_tasks = dict(itertools.groupby(get_running_task_status(), lambda d: d['name']))
            logger.debug('Expected running tasks: %s', Daemons.keys())
            logger.debug('Actual running tasks: %s', running_tasks.keys())
            for daemon in set(Daemons.keys()) - set(running_tasks.keys()):
                logger.info('Spawning {}'.format(daemon))
                Daemons[daemon].run()
    else:
        logger.warning("No mutex supporeted cache backend detected, skipping background tasks executing")


def daemon(restart_duration=10, after_failure='restart', after_success='restart', concurrency=1):
    """
    A always running task
    """
    if restart_duration < 10:
        logger.error("Retry duration for a daemon can't be less than 10s")
        restart_duration = 10

    def wrapper(fn):
        modulename = fn.__module__
        fnname = fn.__name__
        daemon_name = "{}{}".format(modulename, fnname)
        daemon = Daemon(
            fn,
            daemon_name=daemon_name,
            heartbeat_interval=restart_duration
        )
        Daemons[daemon_name] = daemon
        return daemon
    return wrapper


# @worker_shutting_down.connect
# def shutdown_daemons(sender=None, headers=None, body=None, **kwargs):
#     for daemon in Daemons.values():
#         daemon.stop()
