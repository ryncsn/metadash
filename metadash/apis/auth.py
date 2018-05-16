from flask import jsonify, request, Blueprint
from ..auth import get_identity, get_all_users, requires_roles
from ..auth import user_login, user_logout, user_delete, user_setrole
from ..exceptions import APIError

app = Blueprint = Blueprint('authentication', __name__)


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        method = request.json.get('method', None)
    except KeyError:
        return jsonify({'message': 'Missing Credential'}), 400
    try:
        user = user_login(username, password, method)
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
    elif request.method == 'PUT':
        role = request.json.get('role', None)
        user = user_setrole(username, role)
        if user:
            return user.as_dict()
        else:
            return jsonify({'message': 'No such user: "{}"'.format(username)}), 404
