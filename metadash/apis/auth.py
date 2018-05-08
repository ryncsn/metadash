from flask import jsonify, request, Blueprint
from .. import db
from ..auth import get_identity, get_all_users, requires_roles
from ..auth import user_login, user_logout, user_delete
from ..auth.base import User
from ..models import get_or_create
from ..exceptions import APIError

app = Blueprint = Blueprint('authentication', __name__)


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
    except KeyError:
        return jsonify({'message': 'Missing Credential'}), 400
    try:
        user = user_login(username, password)
    except APIError as error:
        return jsonify({'message': error.message}), 400
    else:
        if not user:
            return jsonify({'message': 'Login Failed'}), 400
        else:
            ident = get_identity()
            ident.update({'message': 'Login Success'})
            return jsonify(ident)


@app.route('/logout', methods=['GET'])
def logout():
    try:
        user_logout()
        ident = get_identity()
        ident.update({'message': 'Logout Success'})
    except APIError as error:
        return jsonify({'message': error.message}), 400
    else:
        return jsonify(ident), 200


@app.route('/me', methods=['GET'])
def whoami():
    return jsonify(get_identity()), 200


@app.route('/users', methods=['GET'])
def users():
    return jsonify(get_all_users())


@app.route('/users/<username>', methods=['PUT', 'DELETE'])
@requires_roles('admin')
def user(username):
    if request.method == 'DELETE':
        user_delete(username)
    else:
        role = request.json.get('role', None)
        u, _ = get_or_create(db.session, User, username=username)
        if role:
            u.role = role
    db.session.commit()
    return jsonify({
        "username": u.username,
        "role": u.role
    })
