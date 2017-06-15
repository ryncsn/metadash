from flask import jsonify, session, request, Blueprint
from .. import db
from ..auth import get_identity, get_all_users, requires_roles
from ..auth.ldap import try_login
from ..auth.user import User
from ..exceptions import AuthError
from ..models import get_or_create

app = Blueprint = Blueprint('authentication', __name__)


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
        ident = get_identity()
        ident.update({'message': 'Login Success'})
        return jsonify(ident)


@app.route('/logout', methods=['GET'])
def logout():
    del(session['username'])
    ident = get_identity()
    ident.update({'message': 'Logout Success'})
    return jsonify(ident), 200


@app.route('/me', methods=['GET'])
def whoami():
    return jsonify(get_identity()), 200


@app.route('/users', methods=['GET'])
def users():
    return jsonify(get_all_users())


@app.route('/users/<username>', methods=['PUT', 'POST', 'DELETE'])
@requires_roles('admin')
def user(username):
    if request.method == 'DELETE':
        u = User.query.filter(User.username == username).first_or_404()
        db.session.delete(u)
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
