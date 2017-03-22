import os
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../metadash"))


class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{basedir}/test.db'.format(basedir=basedir)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POLARION_ENABLED = False
    POLARION_URL = '#'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


try:
    from config import ActiveConfig
except ImportError:
    ActiveConfig = DevelopmentConfig
