"""
Basic infrastructures

Provides logging, DB acccess, config etc.
"""
import logging

# Load Flask and config
from flask import Flask
app = Flask(__name__, static_url_path="", static_folder="dist/")

app.config.from_object('config.ActiveConfig')


# setup logging
def _get_logger():
    fmt = '[%(filename)s:%(lineno)d] %(asctime)s %(levelname)s %(message)s'
    loglevel = logging.DEBUG
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


# Load Views
from metadash.apis.result import Blueprint as result # noqa
from metadash.apis.metadata import Blueprint as metadata # noqa
app.register_blueprint(result, url_prefix="/api")
app.register_blueprint(metadata, url_prefix="/api")


# If not catch by any view, fallback to index on non-static
@app.route('/')
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
