"""
Some built in Exceptions
"""
import logging

from sqlalchemy.exc import (
    SQLAlchemyError, NoSuchTableError, IntegrityError, StatementError)

from flask import jsonify
from .. import utils
from .. import logger

logger = logging.getLogger(__name__)


class MetadashAPIError(Exception):
    """
    Used for generate response by raise a exception,
    should be be logged by default for performance issue.

    Extra parameter for __init__ will be logged at debug level
    """
    def __init__(self, message, status_code=None):
        super(MetadashAPIError, self).__init__()
        self.message = message

    def response(self):
        """
        Define how the API should response when certain exception occured
        """
        response = jsonify({
            'message': self.message,
        })
        response.status_code = self.status_code
        return response


APIError = MetadashAPIError


class CriticalError(MetadashAPIError):
    """
    Dont't Panic!
    """
    log_level = logging.CRITICAL
    log_stack = True


class ConfigError(MetadashAPIError):
    """
    Service is not avaliable due to lack of proper config
    """
    log_level = logging.ERROR
    log_stack = True

    status_code = 503


class BadRequestError(MetadashAPIError):
    """
    Wrong parameter, wrong password, etc
    """
    log_level = logging.INFO
    log_stack = False

    status_code = 400


class UnauthorizedError(MetadashAPIError):
    """
    Let the user login
    """
    log_level = logging.INFO
    log_stack = False

    status_code = 401


class RemoteAuthError(MetadashAPIError):
    """
    Remote server rejected our request for authentication error
    """
    log_level = logging.WARN
    log_stack = False

    def __init__(self, mech, message):
        self.mech = mech
        self.message = message

    def response(self):
        """
        An helper to auto reauth for remote authentication error
        eg. We have a keytab, and the exception occured because previous ticket
        expired, just reauth use the keytab.
        """
        if self.mech == 'global-kerberos':
            try:
                utils.kinit()
            except RuntimeError as error:
                response = jsonify({
                    'message': 'Kerberos init failed with "{}"'.format(error),
                })
            except Exception as error:
                response = jsonify({
                    'message': 'Kerberos authentication failed.'.format(error, error.message),
                })
            else:
                response = jsonify({
                    'message': 'Kerberos crenditional expired ({}) and just refreshed, please refresh this page to try again.'.format(self),
                })
                response.status_code = 202
            return response
        else:
            return super(RemoteAuthError, self).response()

    status_code = 502


class RemoteServerError(MetadashAPIError):
    """
    Metadash somehow looks like a proxy, so it can give 504 error
    if remote server failed to response.
    """
    log_level = logging.WARN
    log_stack = False

    status_code = 504


class DependencyError(MetadashAPIError):
    log_level = logging.CRITICAL
    log_stack = True

    status_code = 503


def response_exception(error):
    if error.log_stack:
        logger.exception("Metadash exception occured during process request:")
    logger.log(error.log_level, error.message)
    return error.response()


def response_sqlalchemy_exception(error):
    logger.exception("SQLAlchemy exception occured during process request:")
    if isinstance(error, IntegrityError):
        response = jsonify({
            'message': 'Failed create new data, maybe the object you are tring to create already exists, or it is refering a non exist object.',
        })
        response.status_code = 409
    elif isinstance(error, NoSuchTableError):
        response = jsonify({
            'message': 'Failed querying for data, can\'t find required table.',
        })
        response.status_code = 404
    elif isinstance(error, StatementError):
        response = jsonify({
            'message': 'Failed querying for data, there might be something wrong with your input.',
        })
        response.status_code = 400
    else:
        response = jsonify({
            'message': 'Unknown Database error, please check your input.',
        })
        response.status_code = 500
    return response


def init_app(app):
    @app.errorhandler(MetadashAPIError)
    def handle_metadash_error(error):
        return response_exception(error)

    @app.errorhandler(SQLAlchemyError)
    def handler_sqlalchemy_error(error):
        return response_sqlalchemy_exception(error)
