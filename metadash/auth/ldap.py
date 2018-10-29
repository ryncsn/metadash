from __future__ import absolute_import

from ldap3 import Server, Connection, ALL

from .base import User, AuthBase, AuthError
from .. import db
from ..models import get_or_create
from metadash import app


def get_ldap_server():
    return Server(app.config['LDAP_SERVER'], get_info=ALL)


class LDAPAuth(AuthBase):
    """
    Authentication using an external LDAP server
    If the user doesn't exist in local user table, create a new user with default role.
    """
    @staticmethod
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
