"""
Config manager
"""
import os
import itertools
from .model import ConfigItem as ConfigItemModel
from ..exceptions import ConfigError
from ..models import db, get_or_create
from .. import logger

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../metadash"))


class ConfigItem(object):
    def __init__(self, key, value=None, **kwargs):
        self.description = kwargs.pop("description", "No description")
        self.nullable = kwargs.pop("nullable", False)
        self.default = kwargs.pop("default", None)
        self.secret = kwargs.pop("secret", False)

        # different plugin can't have same key for a plugin
        # the plugin attribute here is just a info for config page
        self.plugin = kwargs.pop("plugin", None)

        if kwargs:
            raise ConfigError("Unrecognized params: {}".format(",".join(kwargs.keys())))

        self.value = value or self.default
        self.key = key

    def validate(self):
        """
        raise ConfigError if invalid
        """
        if self.nullable is False and self.value is None:
            raise ConfigError("Config {} don't have a value"
                              .format(self.key))


class Config(object):
    __all__ = {
        # Public config, for metadash or shared between plugins.
        # Can be viewed direct from config page.
        # All configs are loaded into memory at all time
    }

    def init():
        """
        Initialize the DB backend independently.
        """
        session = db.create_scoped_session()
        ConfigItemModel.__table__.create(session.bind, checkfirst=True)
        session.commit()

    @staticmethod
    def save():
        """
        Save to database
        """
        session = db.create_scoped_session()
        for key, item in Config.__all__.items():
            if item.secret:
                continue
            db_instance = get_or_create(session, ConfigItemModel, key=key)
            db_instance.value = item.value
        session.commit()

    @staticmethod
    def load():
        """
        Load from database,
        only load existing config items.
        """
        session = db.create_scoped_session()
        for db_instance in session.query(ConfigItemModel).filter(
                ConfigItemModel.key.in_(Config.__all__.keys())).all():
            Config.__all__[db_instance.key].value = db_instance.value
        session.commit()

    @staticmethod
    def get_config(key):
        """
        Get configs by name
        """
        ret = Config.__all__.get(key)
        if not ret:
            raise ConfigError("Trying to access non-exist config item {}"
                              .format(key))

    @staticmethod
    def get_plugins():
        """
        Get configs grouped by Plugins
        """
        return itertools.groupby(Config.__all__, lambda x: x.plugin)

    @staticmethod
    def get(key):
        """
        Get value of a config item
        """
        ret = Config.__all__.get(key)
        if not ret:
            raise ConfigError("Trying to access non-exist config item {}"
                              .format(key))
        ret.validate()
        return ret.value

    @staticmethod
    def set(key, value):
        """
        Set value of a config item
        """
        ret = Config.__all__.get(key)
        if not ret:
            raise ConfigError("Trying to access non-exist config item {}"
                              .format(key))
        ret.value = Config.__all__.get(key)

    @staticmethod
    def create(key, **params):
        """
        Create a config item
        """
        item = ConfigItem(key, **params)
        ret = Config.__all__.setdefault(key, item)
        if id(item) != id(ret):
            raise ConfigError("Conflict with config item {}"
                              .format(key))
        return ret
