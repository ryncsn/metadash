import config
from flask import jsonify
from functools import wraps


def get_current_user_role():
    if config.SECURITY is None:
        return "admin"
    else:
        raise NotImplementedError()


def requires_roles(*roles):
    # Allow admin to do anything
    if "admin" not in roles:
        roles = ["admin"].extend(roles)

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                return jsonify({"message": "Not authorized"}, 401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper
