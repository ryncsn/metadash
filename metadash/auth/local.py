from __future__ import absolute_import

import re

from werkzeug.security import generate_password_hash, check_password_hash

from .base import User, AuthBase, AuthError
from .. import db
from ..models import get_or_create


class LocalUser(db.Model):
    # At least 8 characters, contains at least one alphabet and one digit
    PASSWORD_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

    uuid = db.Column(db.ForeignKey(User.uuid), primary_key=True)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, uuid, password):
        self.uuid = uuid
        self.set_password(password)

    def validate_password(self, password):
        return self.PASSWORD_RE.match(password) is not None

    def set_password(self, password):
        if not self.validate_password(password):
            raise AuthError("Password invalid, "
                            "password should be at least 8 characters long "
                            "and contains one alphabet and one digit.")
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class LocalAuth(AuthBase):
    @staticmethod
    def try_login(username, password):
        session = db.create_scoped_session()
        user = session.query(User).filter(User.username == username).first()
        if user:
            local_user = session.query(LocalUser).filter(LocalUser.uuid == user.uuid).first()
        else:
            local_user = None

        if local_user is not None and local_user.check_password(password):
            return user

        raise AuthError("Invalid username or password")

    @staticmethod
    def try_signup(username, password):
        session = db.create_scoped_session()
        user, created = get_or_create(session, User, username=username)
        if not created:
            raise AuthError("Invalid username or username already exist.")

        localuser, _ = get_or_create(session, LocalUser, uuid=user.uuid, password=password)
        session.commit()

        return user

    @staticmethod
    def try_delete(uuid):
        session = db.create_scoped_session()
        user = session.query(User).filter(User.uuid == uuid)

        if user is None:
            raise AuthError("User doesn't exist.")

        localuser = session.query(LocalUser).filter(LocalUser.uuid == uuid)

        session.delete(localuser)
        session.delete(user)
        session.commit()

        return user
