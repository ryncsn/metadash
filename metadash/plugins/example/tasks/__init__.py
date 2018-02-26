import time

from metadash.async import task, daemon
from metadash.async.task import update_task_info


@task()
def long_running(sleep_time):
    for i in range(sleep_time):
        update_task_info("RUNNING", "Sleeping (%s/%s)" % (i, sleep_time))
        time.sleep(1)
    return {
        "message": "Done!"
    }


@daemon()
def time_counter(self):
    self.keep_running = True
    while self.keep_running:
        time.sleep(1)


@time_counter.on_exit
def time_counter_stop(self):
    self.keep_running = False
