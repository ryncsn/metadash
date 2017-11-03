"""
Default config file that controls the whole project.
This file hold the configures that should be only visible at server side
and should be changed at runtime, like DB backend URL and secret key values.

This file is only intend to be used for server setup, for any other configs,
like user/password/3rd part API url, use Database, or metadash.config.
"""

import os
from metadash.config import Config
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../metadash"))


class ActiveConfig(Config):
    DEBUG = True
    TESTING = False
    SECRET_KEY = ''  # Replace it
    SECURITY = False
    CACHE_DEFAULT_BACKEND = 'dogpile.cache.redis'
    CACHE_ARGUEMENTS = {
        'host': 'redis',
        'port': 6379,
        'db': 0,
        'redis_expiration_time': 60 * 60 * 24,   # 24 hours
        'distributed_lock': True
    }
    DEFERD_ENABLED = False
    DEBOUNCE_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'postgresql://metadash:password@postgres/metadash'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
