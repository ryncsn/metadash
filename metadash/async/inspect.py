from .task import celery

AsyncResult = celery.AsyncResult


def get_active_workers():
    # Get all running (active) jobs grouped by worker
    workers = celery.control.inspect().active()
    if workers is None:
        return {}
    return workers


def get_running_task_status():
    task_status = []
    workers = get_active_workers()
    for worker, tasks in workers.items():
        for task in tasks:
            res = AsyncResult(task['id'])
            task_status.append({
                'name': task['name'],
                'id': task['id'],
                'state': res.state,
                'meta': res.info
            })
    return task_status


def cancel_task(task_ids=[]):
    task_status = {}
    worker_tasks = get_active_workers()
    for worker, tasks in worker_tasks.items():
        for task in tasks:
            res = AsyncResult(task['id'])
            task_status[task['name']] = {
                'state': res.state,
                'meta': res.info
            }
            if task['id'] in task_ids:
                res.revoke(terminate=True)
                task_status[task['name']]['canceled'] = True
    return task_status
