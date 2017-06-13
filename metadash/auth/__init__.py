from flask import jsonify, session, request, Blueprint, abort, make_response
from functools import wraps
from .ldap import try_login
from ..exceptions import AuthError
from config import ActiveConfig as config


app = Blueprint = Blueprint('authentication', __name__)


def get_ident():
    return {
        'username': session.get('username') or None,
        'role': session.get('role') or 'anonymous',
    }


def get_current_user_role():
    if config.SECURITY is None:
        return 'admin'
    else:
        return session.get('role') or 'anonymous'


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


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
    except KeyError:
        return jsonify({'message': 'Missing Credential'}), 400
    try:
        user = try_login(username, password)
    except AuthError:
        return jsonify({'message': 'Invalid Credential'}), 400
    else:
        session['username'] = user.username
        session['role'] = user.role
        ident = get_ident()
        ident.update({'message': 'Login Success'})
        return jsonify(ident)


@app.route('/logout', methods=['GET'])
def logout():
    del(session['username'])
    del(session['role'])
    ident = get_ident()
    ident.update({'message': 'Logout Success'})
    return jsonify(ident)


@app.route('/me', methods=['GET'])
def whoami():
    return jsonify(get_ident())
