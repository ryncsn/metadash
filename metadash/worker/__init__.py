"""
Start async workers based on Celery

@deferred for *simple task used to get property of entity*, like a functoin
that perform a http request to remote resource and return, suppose to be IO
jobs (which mean won't bring much workload for the main thread), and will run
in sub thread, non-blocking until the main thread try to jsonify the result,
so multiple request can be performance the same time.

Will return a asyncio Future object, and start execution on create, retrive
or wait use .result(None)

@task for *complex task*, like a bulk update of whole database, or any long
running task, will be dispatched to workers (Celery worker).

Schedule when called with .delay(), retrive or wait use .wait()
"""
from .deferred import deferred
from .task import task, update_task_info
from .daemon import daemon

__all__ = ['deferred', 'task',
           'update_task_info', 'daemon']
