"""
Helper to define Temporary Entity models.
"""

import uuid

from sqlalchemy import event
from sqlalchemy.ext.associationproxy import association_proxy

from .. import db
from ..types import UUID

from .utils import _get_table_name_dict
from .utils import _format_for_json, _Jsonable
from .entity import MetadashEntity, URN


class TemporaryEntityMeta(type(db.Model)):
    """
    Custom metaclass for creating new TemporaryEntity.
    """
    pass


# pylint: disable=no-member
class TemporaryEntityModel(metaclass=TemporaryEntityMeta):
    """
    A temporary entiry
    """
    pass
