from flask import jsonify, Blueprint
from metadash.async.inspect import get_active_workers, get_running_task_status


app = Blueprint = Blueprint('tasks', __name__)


@app.route("/tasks")
def tasks():
    tasks = get_running_task_status()
    return jsonify(tasks)


@app.route("/workers")
def workers():
    workers = get_active_workers()
    return jsonify(workers)
