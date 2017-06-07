"""
Configures, if ./config.py exists, will be overrieded
"""

import os
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../metadash"))


class Config(object):
    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{basedir}/test.db'.format(basedir=basedir)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configures that will exposed to frontend
    PUBLICS = {
    }

    # Results
    RESULTSDB_API = ''


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
