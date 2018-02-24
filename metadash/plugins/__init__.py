"""
Plugin loader
"""
from flask import Blueprint
from metadash import logger
from metadash.injector import NoServiceError
from metadash.config import load_meta as load_config_meta
from metadash.models.base.attribute import init as init_relation

import importlib
import json
import os

# TODO: Allow to disable some plugin without removing them
Loaded = {
    # How it looks:
    # "example-plugin": {
    #     "module": <class 'metadash.plugins.example-plugin'>,
    #     "import": "metadash.plugins.example-plugin",
    # }
}
plugin_base = os.path.dirname(os.path.abspath(__file__))


def get_plugin_names():
    """
    Find all valid plugin folder under `plugin_base`
    Only folder contains a plugin.json is considered a plugin folder
    """
    plugin_names = [dir_
                    for dir_ in os.listdir(plugin_base)
                    if os.path.isdir(os.path.join(plugin_base, dir_)) and
                    os.path.isfile(os.path.join(plugin_base, dir_, 'plugin.json'))]
    return plugin_names


def process_configs(plugin_meta):
    """
    Load configurable parameters from a plugin
    """
    plugin_name = plugin_meta['name']
    config_meta = plugin_meta.get("configs")
    load_config_meta(config_meta, plugin_name)


def meta_loader(plugin_dir, app):
    """
    Load metadata (plugin.json) of a plugin
    """
    with open(os.path.join(plugin_base, plugin_dir, "plugin.json")) as meta_file:
        plugin_meta = json.load(meta_file)
        if not plugin_meta.get('name'):
            logger.error('Plugin {} don\'t have a valid name!'.format(plugin_dir))
            raise RuntimeError('Plugin name invalid')
        elif plugin_meta.get('name') in Loaded.keys():
            logger.error('Plugin {} name conflict!'.format(plugin_dir))
            raise RuntimeError('Plugin name conflict')

        try:
            process_configs(plugin_meta)

            # XXX: strange workaround for sqlalchemy dialect loading
            importpath = "metadash.plugins.{}".format(plugin_dir)
            setattr(Plugins, plugin_dir, importlib.import_module(importpath))

            module = importlib.import_module("metadash.plugins.{}".format(plugin_dir))
            if hasattr(module, 'regist'):
                module.regist(app)
            Loaded[plugin_meta['name']] = {
                "module": module,
                "import": importpath
            }
        except Exception:
            # Just crash on plugin loading error, it's trouble some to clean up a failed plugin
            logger.error("Got exception during initializing plugin: {}".format(plugin_meta["name"]))
            raise
        return plugin_meta


def model_loader(plugin_name):
    """
    Load and regist models (SQLAlchemy Models) of a plugin.
    """
    models_path = os.path.join(plugin_base, plugin_name, 'models')
    if os.path.isfile(os.path.join(models_path, "__init__.py")):
        importlib.import_module("metadash.plugins.{}.models".format(plugin_name))


def task_loader(plugin_name):
    """
    Load and regist models (SQLAlchemy Models) of a plugin.
    """
    models_path = os.path.join(plugin_base, plugin_name, 'tasks')
    if os.path.isfile(os.path.join(models_path, "__init__.py")):
        importlib.import_module("metadash.plugins.{}.tasks".format(plugin_name))


def api_loader(plugin_name, app):
    """
    Load and regist APIs (Flask Blueprint) of a plugin.
    """
    apis_path = os.path.join(plugin_base, plugin_name, 'apis')
    if os.path.isfile(os.path.join(apis_path, "__init__.py")):
        apis = importlib.import_module("metadash.plugins.{}.apis".format(plugin_name))
        blueprint = apis.Blueprint
        app.register_blueprint(blueprint, url_prefix="/api")


def resolve_deps_loading(plugins: list, loader):
    """
    Load a list of plugins using given loader, skip a plugin loading if
    loader raised a NoServiceError, then try to load the plugin again
    in next iteration. Will try to load all plugins for `loop_limit` times.

    This should be able so solve some simple dependency problem.
    """
    plugins_to_load = plugins.copy()

    loop_limit = 30

    while plugins_to_load:
        plugin = plugins_to_load.pop(0)
        try:
            loader(plugin)
        except NoServiceError:
            if not loop_limit:
                raise
            plugins_to_load.append(plugin)
        finally:
            loop_limit -= 1


class Plugins(dict):
    @classmethod
    def get_all(cls):
        return Loaded

    @staticmethod
    def regist(app):
        """
        Entry point for plugin initialization
        """
        plugins = get_plugin_names()

        resolve_deps_loading(
            plugins,
            lambda plugin: meta_loader(plugin, app))

        resolve_deps_loading(
            plugins,
            lambda plugin: model_loader(plugin))

        # Initialize the relation between entities and attributes
        init_relation()

        resolve_deps_loading(
            plugins,
            lambda plugin: task_loader(plugin))

        resolve_deps_loading(
            plugins,
            lambda plugin: api_loader(plugin, app))

        logger.info("Loaded Plugins {}".format(list(Loaded.keys())))


Blueprint = Blueprint('result', __name__)
