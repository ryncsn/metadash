"""
Helper to define Singleton Entity models.
"""

# TODO: require a singleton entity should return a instance
import uuid

from sqlalchemy import event
from sqlalchemy.ext.associationproxy import association_proxy

from .. import db
from ..types import UUID

from .utils import _get_table_name_dict
from .utils import _format_for_json, _Jsonable
from .entity import MetadashEntity, URN


class SingletonEntityMeta(type(db.Model)):
    """
    Custom metaclass for creating new SingletonEntity.
    """
    pass


# pylint: disable=no-member
class SingletonEntityModel(metaclass=SingletonEntityMeta):
    """
    A singleton entiry

    Need to provide a __namespace__ to identify it.
    __namespace__ should be either a UUID or a string, which will be
    hashed into a uuid5.
    """
    pass
