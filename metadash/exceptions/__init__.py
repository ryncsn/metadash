"""
Some built in Exceptions
"""
from flask import jsonify
from .. import logger


class MetadashException(Exception):
    def __init__(self, *args, **kwargs):
        super(MetadashException, self).__init__(*args, **kwargs)

    @property
    def message(self):
        return " ".join(self.args) if len(self.args) != 0 else "Unknown Error"

    handlers = []
    status_code = 500


class CriticalError(Exception):
    """
    Dont't Panic!
    """
    handlers = []


class ConfigError(MetadashException):
    """
    Service is not avaliable due to lack of proper config
    """
    handlers = []
    status_code = 503


class AuthError(MetadashException):
    """
    Just let the user login
    """
    handlers = []
    status_code = 401


class RemoteAuthError(MetadashException):
    """
    Remote server rejected our request for authentication error,
    Metadash should be able to handle it and try again, but if
    it failed, maybe 511 code could be used?
    """
    handlers = []
    status_code = 511


class RemoteServerError(MetadashException):
    """
    Metadash somehow looks like a proxy, so it can give 504 error
    if remote server failed to response.
    """
    handlers = []
    status_code = 504


class DependencyError(MetadashException):
    handlers = []
    status_code = 503


def init_app(app):
    @app.errorhandler(MetadashException)
    def handle_invalid_usage(error):
        response = jsonify({
            'message': error.message,
        })
        response.status_code = error.status_code
        logger.exception(error)
        return response
