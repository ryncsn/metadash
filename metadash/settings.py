"""
Default application settings
This file hold the secret settingures that should not be accessable to anyone by the server admin
and won't be changed at runtime, like DB backend URL and secret key values.

Settings here could be overrided by enviroment variables.
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


class AppSettings(object):
    """
    Default values for setup development server
    """
    _ENV_PREFIX = 'APP_'
    RELATIVE_PATH = ''

    DEBUG = False
    SECURITY = True
    DEVELOPMENT = False
    TESTING = False
    SECRET_KEY = ''  # Replace with some random string please
    DEFAULT_AUTH_BACKEND = 'local'

    API_PATH = None  # Hinting
    STATIC_PATH = None  # Hinting

    # SQL Database URI format: "${DATABASE_ENGINE}://${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_SERVICE}/${DATABASE_NAME}"
    # or (without authentication): "${DATABASE_ENGINE}://${DATABASE_SERVICE}/${DATABASE_NAME}"
    # Use Sqlite as default for development and demo
    SQL_DATABASE_URI = 'sqlite:///{basedir}/test/test.db'.format(basedir=basedir)
    # Redis URI format: "redis://:${REDIS_PASSWORD}@${REDIS_SERVICE}:${REDIS_PORT}"
    # Use empty as default for development and demo, so async tasks won't work, and caching will use memory as the backend
    REDIS_URI = ''
    # For distributed lock when redis is used
    REDIS_LOCK_TIMEOUT = 60

    # !!! Following attributed will be overrided according to attributes above
    # Refer to function initialize for more detail
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_ECHO = False
    CACHE_DEFAULT_BACKEND = ''
    CACHE_ARGUEMENTS = {}
    CELERY_BROKER_URL = ''
    CELERY_RESULT_BACKEND = ''

    @classmethod
    def update_from_env(settings):
        """
        Override from Env
        """
        for attr_name in dir(settings):
            if attr_name.startswith('_') or attr_name.upper() != attr_name:
                continue

            orig_value = getattr(settings, attr_name)
            is_required = isinstance(orig_value, Required)
            orig_type = orig_value.v_type if is_required else type(orig_value)
            env_var_name = settings._ENV_PREFIX + attr_name
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
                setattr(settings, attr_name, env_var)
            elif is_required:
                raise RuntimeError('The required environment variable "{0}" is currently not set'
                                   .format(env_var_name))

    @classmethod
    def initialize(settings):
        """
        Some common checks and load default values
        """
        settings.API_PATH = settings.RELATIVE_PATH + '/api'
        settings.STATIC_PATH = settings.RELATIVE_PATH + '/static'

        if not settings.SECRET_KEY:
            logger.critical("Remember to set your non-empty secret value for production!")
            if not AppSettings.DEVELOPMENT:
                raise RuntimeError("Please set your secret key (env SECRET_KEY), or use development mode (env APP_DEVELOPMENT=true)!")
            else:
                logger.warning("Using development secret key, this is only supposed to be used with a development server.")
                settings.SECRET_KEY = "DEVELOPEMENT"

        if not AppSettings.REDIS_URI:
            logger.warning('Redis is required for distribute async tasks to workers and high performance caching')
            if not AppSettings.DEVELOPMENT:
                raise RuntimeError("Redis is required for production enviroment")

        settings.SQLALCHEMY_DATABASE_URI = settings.SQL_DATABASE_URI

        if settings.REDIS_URI:
            URI_RE = r'redis://(?:(?P<user>[^:@]*)?(?::(?P<password>[^@]*))?@)?(?P<host>[^:/]+)(?::(?P<port>\d+))?/?'
            _user, password, host, port = re.match(URI_RE, settings.REDIS_URI).groups()
            settings.CACHE_DEFAULT_BACKEND = "dogpile.cache.redis"
            settings.CACHE_ARGUEMENTS = {
                "distributed_lock": True,
                "lock_timeout": 60,
                "host": host,
                "password": password or '',
                "port": port or 6379
            }
            settings.CELERY_BROKER_URL = settings.REDIS_URI
            settings.CELERY_RESULT_BACKEND = settings.REDIS_URI
        else:
            settings.CACHE_DEFAULT_BACKEND = "dogpile.cache.memory"
            settings.CACHE_ARGUEMENTS = {}
            settings.CELERY_BROKER_URL = ''
            settings.CELERY_RESULT_BACKEND = ''
