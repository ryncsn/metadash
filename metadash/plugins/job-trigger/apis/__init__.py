import requests

from flask import Blueprint, request, redirect
from metadash.config import Config
from metadash import logger

app = Blueprint = Blueprint("jobs", __name__)


@app.route("/get-jobs", methods=["POST"])
def get_jobs():
    res = requests.post(Config.get("GET_JOBS_URL"), request.json)
    res.raise_for_status()
    return res.text


@app.route("/trigger-jobs", methods=["POST"])
def trigger_jobs():
    res = requests.post(Config.get("TRIGGER_JOBS_URL"), request.json)
    res.raise_for_status()
    return res.text