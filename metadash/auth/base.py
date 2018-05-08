"""
Base model of a user
"""
from uuid import uuid1

from .. import db
from ..models.types import UUID
from ..exceptions import APIError


class AuthError(APIError):
    pass


class User(db.Model):
    """
    Base User model and table definition, when inheriting from this class,
    please don't add extra column, migration of this part is not supported yet.
    """
    ROLES = ['admin', 'user', 'anonymous']

    __tablename__ = 'metadash-users'

    username = db.Column(db.String(), nullable=False, unique=True)
    uuid = db.Column(UUID, default=uuid1, primary_key=True)
    role = db.Column(db.Enum(*ROLES, name="user_roles"), nullable=False, default='anonymous')

    def __init__(self, username=None, uuid=None, role=None):
        self.username = username
        self.uuid = uuid or uuid1()
        self.role = role or 'anonymous'

    def as_dict(self):
        return {
            'uuid': self.uuid,
            'username': self.username,
            'role': self.role
        }


class AuthBase(object):
    """
    Base class for authentication
    """
    ROLES = User.ROLES

    @staticmethod
    def try_login(username, password):
        """
        Raise AuthError on failure, else return a User model instance
        """
        if False:  # If Login failed
            raise AuthError("Impossible Error")
        raise NotImplementedError()

    @staticmethod
    def try_signup(username, password):
        """
        Raise AuthError on failure, else return a User model instance
        """
        if False:  # If Authentication failed
            raise AuthError("Impossible Error")
        raise NotImplementedError()

    @staticmethod
    def try_delete(username, password):
        """
        Delete callback

        Raise AuthError on failure, else return a User model instance
        """
        if False:  # If Delete failed
            raise AuthError("Impossible Error")
        raise NotImplementedError()
