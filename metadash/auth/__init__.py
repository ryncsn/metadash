from flask import jsonify, session, request, Blueprint, abort, make_response
from functools import wraps
from .ldap import try_login
from ..exceptions import AuthError
from config import ActiveConfig as config
from .user import User
from .. import db


app = Blueprint = Blueprint('authentication', __name__)


def get_ident():
    return {
        'username': session.get('username') or None,
        'role': session.get('role') or 'anonymous',
    }


def get_current_user_role():
    if not config.SECURITY:
        return 'admin'
    else:
        username = session.get('username')
        if username:
            return User.query.filter(User.username == username).first().role
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
        ident = get_ident()
        ident.update({'message': 'Login Success'})
        return jsonify(ident)


@app.route('/logout', methods=['GET'])
def logout():
    del(session['username'])
    ident = get_ident()
    ident.update({'message': 'Logout Success'})
    return jsonify(ident)


@app.route('/me', methods=['GET'])
def whoami():
    return jsonify(get_ident())


@app.route('/users', methods=['GET'])
def users():
    return jsonify([{
        "username": u.username,
        "role": u.role
    } for u in User.query.all()])


@app.route('/users/<username>', methods=['PUT'])
@requires_roles('admin')
def user(username):
    role = request.json['role']
    u = User.query.filter(User.username == username).first()
    u.role = role
    db.session.commit()
    return jsonify({
        "username": u.username,
        "role": u.role
    })


