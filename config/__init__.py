"""
Default config file that controls the whole project.
This file hold the configures that should be only visible at server side
and should be changed at runtime, like DB backend URL and secret key values.

This file is only intend to be used for server setup, for any other configs,
like user/password/3rd part API url, use Database, or metadash.config.
"""

import logging
import os
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../metadash"))

logger = logging.getLogger(__name__)


class Config(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = ''  # Replace with some random string please
    SECURITY = False
    CACHE_DEFAULT_BACKEND = 'dogpile.cache.memory'
    CACHE_ARGUEMENTS = {}

    CELERY_BROKER_URL = 'redis://localhost:6379',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{basedir}/test.db'.format(basedir=basedir)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True


try:
    from .config import ActiveConfig
except ImportError:
    ActiveConfig = DevelopmentConfig


# Some common checks
if not ActiveConfig.SECRET_KEY:
    ActiveConfig.SECRET_KEY = ''
    logger.warning("Using empty secret key, this is only supposed to be used with a development server.")
    if not ActiveConfig.DEVELOPMENT:
        raise RuntimeError("Please set your secret key value for production!")

if not ActiveConfig.CELERY_BROKER_URL:
    logger.error('Need a backend broker for celery to work, or tasks won\'t get scheduled.')
