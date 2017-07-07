from flask import jsonify, session, abort, make_response
from functools import wraps
from config import ActiveConfig as config
from .user import User


def _format_user(user):
    return {
        "username": user.username,
        "role": user.role
    }


def get_identity():
    username = session.get('username')
    user_instance = User.query.filter(User.username == username).first()
    user_role = user_instance and user_instance.role or 'anonymous'
    return {
        'username': session.get('username') or None,
        'role': user_role
    }


def get_current_user_role():
    """
    Get role of current loged in user, or return 'admin' if
    SECURITY is set to False
    """
    if not config.SECURITY:
        return 'admin'
    else:
        username = session.get('username')
        if username:
            user = User.query.filter(User.username == username).first()
            if not user:
                del session['username']
                return 'anonymous'
            else:
                return user.role
        else:
            return 'anonymous'


def requires_roles(*roles):
    # Allow admin to do anything
    if 'admin' not in roles:
        roles = ['admin'] + list(roles)

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                abort(make_response(
                    jsonify({'message': 'Not authorized'}), 401))
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def get_all_users(*roles):
    return [_format_user(u) for u in User.query.all()]
