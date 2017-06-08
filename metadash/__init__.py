"""
Basic infrastructures

Provides logging, DB acccess, config etc.
"""
import logging
import config

# Load Flask and config
from flask import Flask, jsonify
app = Flask(__name__, static_url_path="", static_folder="dist/")

app.config.from_object('config.ActiveConfig')


# setup logging
def _get_logger():
    fmt = '%(pathname)s:%(lineno)d %(asctime)s %(levelname)s %(message)s'
    loglevel = logging.DEBUG  # TODO: in config
    formatter = logging.Formatter(fmt=fmt)

    root_logger = logging.getLogger('metadb')
    root_logger.setLevel(loglevel)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    return root_logger


logger = _get_logger()


# Load ORM
from flask_sqlalchemy import SQLAlchemy # noqa
db = SQLAlchemy(app)


# Load default configs
import json # noqa
import os # noqa
from .config import Config, load_meta # noqa
with app.app_context():
    Config.init()
defaults = os.path.abspath(os.path.join(os.path.dirname(__file__), "./config/defaults.json"))
with open(defaults) as default_configs:
    load_meta(json.load(default_configs))


# Load Views
from metadash.apis.result import Blueprint as result # noqa
from metadash.apis.metadata import Blueprint as metadata # noqa
app.register_blueprint(result, url_prefix="/api")
app.register_blueprint(metadata, url_prefix="/api")


from metadash.plugins import Plugins as plugins # noqa
plugins.regist(app)


@app.route('/config')
def send_config(path):
    return jsonify(config.PUBLIC)


# If not catch by any view, fallback to index on non-static
@app.route('/', defaults={"path": ""})
@app.route('/<path>')
def index(path):
    return app.send_static_file('index.html')
# Then fallback to static files


# Load Manager and Migration
from flask_migrate import Migrate, MigrateCommand # noqa
from flask_script import Manager # noqa
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.cli.command('initdb')
def init_db_cli():
    init_db()


def init_db():
    with app.app_context():
        db.create_all()


# Start the server
if __name__ == '__main__':
    manager.run()
