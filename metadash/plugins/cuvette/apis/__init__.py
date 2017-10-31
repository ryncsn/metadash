import requests

from flask import Blueprint, jsonify
from metadash.config import Config

app = Blueprint = Blueprint("cuvette", __name__)


@app.route("/cuvette-machine-parameters", methods=["GET"])
def get_parameters():
    res = requests.get("{}/parameters".format(Config.get("CUVETTE_URL").rstrip('/')))
    res.raise_for_status()
    return jsonify(res.json())


@app.route("/cuvette-machine-request", methods=["POST"])
def submit_request():
    res = requests.post("{}/machine".format(Config.get("CUVETTE_URL").rstrip('/')))
    res.raise_for_status()
    return jsonify(res.json())
