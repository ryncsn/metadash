import requests
import json

from flask import Blueprint, request, redirect
from metadash.config import Config
from metadash.auth import requires_roles, get_identity
from metadash import logger

app = Blueprint = Blueprint("jobs", __name__)


@app.route("/get-jobs", methods=["POST"])
def get_jobs():
    res = requests.get(Config.get("GET_JOBS_URL"), request.json)
    res.raise_for_status()
    return res.text


@app.route("/trigger-jobs", methods=["POST"])
@requires_roles('user')
def trigger_jobs():
    data = request.json
    ci_message = json.loads(data.setdefault('ci_message', '{}'))
    ci_message['triggered-by'] = get_identity()['username']
    data['ci_message'] = json.dumps(ci_message)
    res = requests.post(Config.get("TRIGGER_JOBS_URL"), json=data)
    res.raise_for_status()
    return res.text
