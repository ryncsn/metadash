"""
Default config file that controls the whole project.
This file hold the configures that should be only visible at server side
and shouldn not be changed at runtime, like DB backend URL and secret key values.

This file is only intend to be used for server setup, for any other configs,
like user/password/3rd API url, see metadash.config.
"""


from . import ProductionConfig


class ActiveConfig(ProductionConfig):

    SECRET_KEY = 'c3VwZXItc2VjcmV0LWtleQo'

    SQL_DATABASE_URI = 'postgresql://metadash:metadash@postgres/metadash'
    REDIS_URI = 'redis://:metadash@redis:6379'
