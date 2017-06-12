from __future__ import absolute_import

from ldap3 import Server, Connection, ALL

from .user import User
from .. import db
from ..models import get_or_create
from ..exceptions import AuthError
from ..config import Config


def get_ldap_server():
    return Server(Config.get('LDAP_SERVER'), get_info=ALL)


# TODO: provide User.try_login
def try_login(username, password):
    session = db.create_scoped_session()
    user, _ = get_or_create(session, User, username=username)
    srv = get_ldap_server()
    conn = Connection(srv, "cn={},ou=Users,dc=redhat,dc=com".format(username), password=password)
    if not conn.bind():
        session.rollback()
        raise AuthError("LDAP: INVALID_CREDENTIALS")
    if _:
        session.commit()
    return user
