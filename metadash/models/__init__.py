import sqlite3

from sqlalchemy.engine import Engine
from sqlalchemy import event

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
