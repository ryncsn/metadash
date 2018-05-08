"""
Default configs and settings
This file hold the configures that should be only visible at server side
and won't be changed at runtime, like DB backend URL and secret key values.

Any config here could be overrided by:

 - appropriate enviroment variable

 - ./config.py in this folder

This file is only intend to be used for server deployment, for any other configs,
like user/password/3rd part API url, use Database, or metadash.config.
"""

import os
import re
import json
import logging

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../metadash"))

logger = logging.getLogger(__name__)


class Required:
    def __init__(self, v_type=None):
        self.v_type = v_type


class Config(object):
    """
    Default values for setup development server
    """
    _ENV_PREFIX = 'APP_'

    DEBUG = True
    TESTING = False
    SECRET_KEY = ''  # Replace with some random string please
    SECURITY = True
    DEVELOPMENT = True
    DEFAULT_AUTH_BACKEND = 'local'

    # SQL Database URI format: "${DATABASE_ENGINE}://${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_SERVICE}/${DATABASE_NAME}"
    # or (without authentication): "${DATABASE_ENGINE}://${DATABASE_SERVICE}/${DATABASE_NAME}"
    # Use Sqlite as default for development and demo
    SQL_DATABASE_URI = 'sqlite:///{basedir}/test.db'.format(basedir=basedir)
    # Redis URI format: "redis://:${REDIS_PASSWORD}@${REDIS_SERVICE}:${REDIS_PORT}"
    # Use empty as default for development and demo, so async tasks won't work, and caching will use memory as the backend
    REDIS_URI = ''
    # For distributed lock when redis is used
    REDIS_LOCK_TIMEOUT = 60

    # !!! Following attributed will be overrided according to attributes above
    # Refer to function initialize for more detail
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''
    CACHE_DEFAULT_BACKEND = ''
    CACHE_ARGUEMENTS = {}
    CELERY_BROKER_URL = ''
    CELERY_RESULT_BACKEND = ''

    @classmethod
    def update_from_env(config):
        """
        Override from Env
        """
        for attr_name in dir(config):
            if attr_name.startswith('_') or attr_name.upper() != attr_name:
                continue

            orig_value = getattr(config, attr_name)
            is_required = isinstance(orig_value, Required)
            orig_type = orig_value.v_type if is_required else type(orig_value)
            env_var_name = config._ENV_PREFIX + attr_name
            env_var = os.getenv(env_var_name, None)
            if env_var is not None:
                if issubclass(orig_type, bool):
                    env_var = env_var.upper() in ('1', 'TRUE')
                elif issubclass(orig_type, dict):
                    env_var = json.loads(env_var) if env_var else {}
                elif issubclass(orig_type, int):
                    env_var = int(env_var)
                elif issubclass(orig_type, bytes):
                    env_var = env_var.encode()
                # could do floats here and lists etc via json
                setattr(config, attr_name, env_var)
            elif is_required:
                raise RuntimeError('The required environment variable "{0}" is currently not set'
                                   .format(env_var_name))

    @classmethod
    def initialize(config):
        """
        Some common checks and load default values
        """
        if not config.SECRET_KEY:
            logger.critical("Remember to set your non-empty secret value for production!")
            if not ActiveConfig.DEVELOPMENT:
                raise RuntimeError("Please set your secret key value for production!")
            else:
                logger.warning("Using development secret key, this is only supposed to be used with a development server.")
                config.SECRET_KEY = "DEVELOPEMENT"

        if not ActiveConfig.REDIS_URI:
            logger.warning('Redis is required for distribute async tasks to workers and high performance caching')
            if not ActiveConfig.DEVELOPMENT:
                raise RuntimeError("Redis is required for production enviroment")

        config.SQLALCHEMY_DATABASE_URI = config.SQL_DATABASE_URI

        if config.REDIS_URI:
            URI_RE = r'redis://(?::(?P<password>.*?)@)?(?P<host>[\w^:\-]+?)(?::(?P<port>\d+))'
            password, host, port = re.match(URI_RE, config.REDIS_URI).groups()
            config.CACHE_DEFAULT_BACKEND = "dogpile.cache.redis"
            config.CACHE_ARGUEMENTS = {
                "distributed_lock": True,
                "lock_timeout": 60,
                "host": host,
                "password": password,
                "port": port
            }
            config.CELERY_BROKER_URL = config.REDIS_URI
            config.CELERY_RESULT_BACKEND = config.REDIS_URI
        else:
            config.CACHE_DEFAULT_BACKEND = "dogpile.cache.memory"
            config.CACHE_ARGUEMENTS = {}
            config.CELERY_BROKER_URL = ''
            config.CELERY_RESULT_BACKEND = ''


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    SECURITY = True
    DEBUG = True
    DEVELOPMENT = True


class SetupConfig(DevelopmentConfig):
    """
    On initial setup, nobody is admin, so turn off security
    so you can modify protected configurations with WebUI or server API,
    then turn security on.
    """
    SECURITY = False


class TestingConfig(Config):
    TESTING = True


# Override from config.py
try:
    from .config import ActiveConfig
except ImportError:
    ActiveConfig = DevelopmentConfig

ActiveConfig.update_from_env()
ActiveConfig.initialize()
