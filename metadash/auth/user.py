import uuid
from .. import db
from ..models.types import UUID


ROLES = ['admin', 'user', 'anonymous']


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(), nullable=False, unique=True)
    uuid = db.Column(UUID, default=uuid.uuid1, primary_key=True)
    role = db.Column(db.Enum(*ROLES, name="user_roles"), nullable=False, default='anonymous')

    @staticmethod
    def try_login(username, password):
        raise NotImplementedError()
