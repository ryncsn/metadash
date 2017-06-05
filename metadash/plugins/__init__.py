"""
Plugin loader
"""
from flask import Blueprint
from metadash import logger

import importlib
import json
import os


ENABLED = []  # TODO: now it's all enabled
plugin_base = os.path.dirname(os.path.abspath(__file__))


def get_plugin_dirs():
    plugin_dirs = [dir_
                   for dir_ in os.listdir(plugin_base)
                   if os.path.isdir(os.path.join(plugin_base, dir_)) and
                   os.path.isfile(os.path.join(plugin_base, dir_, 'plugin.json'))]
    return plugin_dirs


def initialize(app, plugin_dir):
    # components = os.path.join(plugin_dir, 'components')
    # Flask don't care about it's components yet
    models_path = os.path.join(plugin_base, plugin_dir, 'models')
    apis_path = os.path.join(plugin_base, plugin_dir, 'apis')

    with open(os.path.join(plugin_base, plugin_dir, "plugin.json")) as meta:
        plugin = json.load(meta)
        if not plugin.get('name'):
            logger.error('Plugin {} don\'t have a valid name!'.format(plugin_dir))
        elif plugin.get('name') in ENABLED:
            logger.error('Plugin {} name conflict!'.format(plugin_dir))

        try:
            if os.path.isfile(os.path.join(models_path, "__init__.py")):
                models = importlib.import_module("metadash.plugins.{}.models".format(plugin_dir))
            if os.path.isfile(os.path.join(apis_path, "__init__.py")):
                apis = importlib.import_module("metadash.plugins.{}.apis".format(plugin_dir))
                blueprint = apis.Blueprint
                app.register_blueprint(blueprint, url_prefix="/api")
        except Exception:
            # TODO: better log
            raise

        ENABLED.append(plugin['name'])


class Plugins(object):
    @staticmethod
    def regist(app):
        """
        Entry point for plugin initialization
        """
        plugin_dirs = get_plugin_dirs()
        for plugin in plugin_dirs:
            initialize(app, plugin)

        logger.info("Loaded Plugins {}".format(ENABLED))


Blueprint = Blueprint('result', __name__)
