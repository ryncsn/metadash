import logging

from flask import session
from functools import wraps
from config import ActiveConfig as config

from .local import LocalAuth
from .ldap import LDAPAuth
from .base import User, AuthError

from metadash.exceptions import BadRequestError, UnauthorizedError

logger = logging.getLogger(__name__)


AuthBackends = {
    "local": LocalAuth,
    "ldap": LDAPAuth
}

DefaultAuthBackend = config.DEFAULT_AUTH_BACKEND


def user_login(username, password, backend=None):
    try:
        backend = backend or DefaultAuthBackend
        user = AuthBackends[backend].try_login(username, password)
    except NotImplementedError as error:
        raise BadRequestError("Login is not supported by this authentication method")
    except AuthError as error:
        raise BadRequestError(error.message)
    else:
        session['user_uuid'] = user.uuid
    return user


def user_signup(username, password, backend=None):
    try:
        backend = backend or DefaultAuthBackend
        user = AuthBackends[backend].try_signup(username, password)
    except NotImplementedError as error:
        raise BadRequestError("Sign up is not supported by this authentication method")
    except AuthError as error:
        raise BadRequestError(error.message)
    return user


def user_delete(username, password=None, backend=None):
    try:
        backend = backend or DefaultAuthBackend
        user = AuthBackends[backend].try_delete(username, password)
    except NotImplementedError:
        raise BadRequestError("Delete a user is not supported by this authentication method")
    except AuthError:
        raise BadRequestError(AuthError.message)
    return user


def user_setpass(username, password, backend=None):
    raise BadRequestError("Not allowed")


def user_setrole(username, role):
    user = User.query.filter(User.username == username)
    user_instance = user.first()
    if user_instance:
        user_instance.role = role
        user.session.commit()
        return user_instance
    else:
        return None


def user_logout(backend=None):
    del(session['user_uuid'])
    return True


def get_identity():
    user_uuid = session.get('user_uuid')
    user_instance = None
    user_role = 'anonymous'
    username = None
    if user_uuid:
        user_instance = User.query.filter(User.uuid == user_uuid).first()
        if user_instance is not None:
            user_role = user_instance.role
            username = user_instance.username
        else:
            user_uuid = None
            logger.warn("User {} session still active, "
                        "but user permissoin record was deleted".format(user_uuid))
    return {
        'uuid': user_uuid,
        'username': username,
        'role': user_role
    }


def get_all_users():
    users = User.query.all()
    return [u.as_dict() for u in users]


def get_current_username():
    """
    Return None if not logged in
    """
    user_uuid = session.get('user_uuid')
    user_instance = None
    if user_uuid:
        user_instance = User.query.filter(User.uuid == user_uuid).first()
        if user_instance is not None:
            return user_instance.username
        else:
            logger.warn("User {} session still active, "
                        "but user permissoin record was deleted".format(user_uuid))
    return None


def get_current_role():
    """
    Get role of current loged in user, or return 'admin' if
    SECURITY is set to False
    Return 'anonymous' if not logged in
    """
    if not config.SECURITY:
        return 'admin'

    user_uuid = session.get('user_uuid')
    if user_uuid:
        user_instance = User.query.filter(User.uuid == user_uuid).first()
        if user_instance:
            return user_instance.role
        else:
            logger.warn("User {} session still active, "
                        "but user permissoin record was deleted".format(user_uuid))
    return 'anonymous'


def requires_roles(*roles):
    # Allow admin to do anything
    if 'admin' not in roles:
        roles = ['admin'] + list(roles)

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            current_role = get_current_role()
            if current_role not in roles:
                raise UnauthorizedError(
                    "Your current role is {}, which is not "
                    "allowed to perform request operation.".format(current_role))
            return f(*args, **kwargs)
        return wrapped
    return wrapper
