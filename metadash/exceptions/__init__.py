"""
Some built in Exceptions
"""
from sqlalchemy.exc import (
    SQLAlchemyError, NoSuchTableError, IntegrityError, StatementError)

from flask import jsonify
from .. import utils
from .. import logger


class MetadashException(Exception):
    def __init__(self, *args, **kwargs):
        super(MetadashException, self).__init__(*args, **kwargs)
        self.message = " ".join(self.args) if len(self.args) != 0 else "Unknown Error"

    handlers = []
    status_code = 500


class CriticalError(MetadashException):
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
    def __init__(self, mech, message):
        self.mech = mech
        self.message = message

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


def response_exception(error):
    response = jsonify({
        'message': error.message,
    })
    response.status_code = error.status_code

    if isinstance(error, RemoteAuthError):
        if error.mech == 'global-kerberos':
            try:
                utils.kinit()
            except RuntimeError as new_error:
                response = jsonify({
                    'message': 'Kerberos init failed with "{}", caused by "{}"'.format(new_error, error.message),
                })
                response.status_code = error.status_code
            else:
                response = jsonify({
                    'message': 'Kerberos crenditional expired ({}) and just refreshed, please refresh this page to try again.'.format(error),
                })
                response.status_code = 202

    logger.exception(error)
    return response


def response_sqlalchemy_exception(error):
    if isinstance(error, IntegrityError):
        response = jsonify({
            'message': 'Failed create new data, maybe the object you are tring to create already exists, or it is refering a non exist object.',
        })
        response.status_code = 409
    elif isinstance(error, StatementError):
        response = jsonify({
            'message': 'Failed querying for data, there could be something wrong with your input.',
        })
        response.status_code = 400
    else:
        response = jsonify({
            'message': 'Unknown Database error, please check your input.',
        })
        response.status_code = 500
    logger.exception(error)
    return response


def init_app(app):
    @app.errorhandler(MetadashException)
    def handle_metadash_error(error):
        return response_exception(error)

    @app.errorhandler(SQLAlchemyError)
    def handler_sqlalchemy_error(error):
        return response_sqlalchemy_exception(error)
