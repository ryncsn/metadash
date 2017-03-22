import uuid
import sqlite3

from sqlalchemy.engine import Engine
from sqlalchemy import event

from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as postgre_UUID

from metadash import db


def _sqlite_hack():
    """
    Force Sqlite backend to enable foreign key integrity check.
    """
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if type(dbapi_connection) is sqlite3.Connection:  # play well with other DB backends
           cursor = dbapi_connection.cursor()
           cursor.execute("PRAGMA foreign_keys=ON")
           cursor.close()

_sqlite_hack()


#pylint: disable=no-member
class UUID(TypeDecorator):
    """
    Add a native UUID type for sqlalchemy.

    Copy & Pasted from http://docs.sqlalchemy.org/en/latest/core/custom_types.html
    Platform-independent UUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """

    impl = CHAR

    python_type = uuid.UUID

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(postgre_UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_literal_param(self, value, dialect):
        return uuid.UUID(value) if not value is None else None

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


# Helpers for sqlalchemy operations
def get(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    return instance, False


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance, True
