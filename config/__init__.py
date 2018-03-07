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

import json
import logging
import os
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../metadash"))

logger = logging.getLogger(__name__)


class Required:
    def __init__(self, v_type=None):
        self.v_type = v_type


class Config(object):
    """
    Modify the configs here to modify the default value
    """
    _ENV_PREFIX = 'APP_'

    DEBUG = True
    TESTING = False
    SECRET_KEY = ''  # Replace with some random string please
    SECURITY = True
    DEVELOPMENT = True
    CACHE_DEFAULT_BACKEND = 'dogpile.cache.memory'
    CACHE_ARGUEMENTS = {}

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{basedir}/test.db'.format(basedir=basedir)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CELERY_BROKER_URL = 'redis://localhost:6379'
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CELERY_BROKER_URL = ''
    CELERY_RESULT_BACKEND = ''


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True


# Override from config.py
try:
    from .config import ActiveConfig
except ImportError:
    ActiveConfig = DevelopmentConfig

# Override from Env
for attr_name in dir(ActiveConfig):
    if attr_name.startswith('_') or attr_name.upper() != attr_name:
        continue

    orig_value = getattr(ActiveConfig, attr_name)
    is_required = isinstance(orig_value, Required)
    orig_type = orig_value.v_type if is_required else type(orig_value)
    env_var_name = ActiveConfig._ENV_PREFIX + attr_name
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
        setattr(ActiveConfig, attr_name, env_var)
    elif is_required:
        raise RuntimeError('The required environment variable "{0}" is currently not set'
                           .format(env_var_name))


if not ActiveConfig.SECRET_KEY:
    logger.critical("Please set your non-empty secret value for production!")
    ActiveConfig.SECRET_KEY = 'ABCDEFG'  # hmmmm... VERY SECRET

# Some common checks
if not ActiveConfig.SECRET_KEY:
    ActiveConfig.SECRET_KEY = ''
    logger.warning("Using empty secret key, this is only supposed to be used with a development server.")
    if not ActiveConfig.DEVELOPMENT:
        raise RuntimeError("Please set your secret key value for production!")

if not ActiveConfig.CELERY_BROKER_URL:
    logger.error('Need a backend broker for celery to work, or tasks won\'t get scheduled.')
