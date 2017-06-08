"""
Default config file that controls the whole project.
This file hold the configures that should be only visible at server side
and should be changed at runtime, like DB backend URL and secret key values.

This file is only intend to be used for server setup, for any other configs,
like user/password/3rd part API url, use Database, or metadash.config.
"""

import os
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../metadash"))


class Config(object):
    DEBUG = True
    TESTING = False
    SECRET = ""  # Replace with some random string please
    SECURITY = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{basedir}/test.db'.format(basedir=basedir)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


try:
    from .config import ActiveConfig
except ImportError:
    ActiveConfig = DevelopmentConfig


if not ActiveConfig.SECRET:
    raise RuntimeError("Please use a random string for SECRET")
