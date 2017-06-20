"""
Plugin loader
"""
from flask import Blueprint
from metadash import logger
from metadash.config import Config, load_meta

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


def process_configs(plugin_meta):
    plugin_name = plugin_meta['name']
    config_meta = plugin_meta.get("configs")
    load_meta(config_meta, plugin_name)


def init_meta(plugin_dir):
    with open(os.path.join(plugin_base, plugin_dir, "plugin.json")) as meta_file:
        plugin_meta = json.load(meta_file)
        if not plugin_meta.get('name'):
            logger.error('Plugin {} don\'t have a valid name!'.format(plugin_dir))
            raise RuntimeError()
        elif plugin_meta.get('name') in ENABLED:
            logger.error('Plugin {} name conflict!'.format(plugin_dir))
            raise RuntimeError()

        try:
            process_configs(plugin_meta)

            # XXX: strange workaround for sqlalchemy dialect loading
            setattr(Plugins, plugin_dir, importlib.import_module("metadash.plugins.{}".format(plugin_dir)))
        except Exception:
            # Just crash on plugin loading error, it's trouble some to clean up a failed plugin
            logger.error("Got exception during initializing plugin: {}".format(plugin_meta["name"]))
            raise
        ENABLED.append(plugin_meta['name'])
        return plugin_meta


def init_modal(plugin_dir):
    models_path = os.path.join(plugin_base, plugin_dir, 'models')
    if os.path.isfile(os.path.join(models_path, "__init__.py")):
        importlib.import_module("metadash.plugins.{}.models".format(plugin_dir))


def init_api(plugin_dir, app):
    apis_path = os.path.join(plugin_base, plugin_dir, 'apis')
    if os.path.isfile(os.path.join(apis_path, "__init__.py")):
        apis = importlib.import_module("metadash.plugins.{}.apis".format(plugin_dir))
        blueprint = apis.Blueprint
        app.register_blueprint(blueprint, url_prefix="/api")


class Plugins(object):
    @staticmethod
    def regist(app):
        """
        Entry point for plugin initialization
        """
        plugin_dirs = get_plugin_dirs()

        for plugin in plugin_dirs:
            init_meta(plugin)

        for plugin in plugin_dirs:
            init_modal(plugin)

        for plugin in plugin_dirs:
            init_api(plugin, app)

        logger.info("Loaded Plugins {}".format(ENABLED))


Blueprint = Blueprint('result', __name__)
