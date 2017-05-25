"""
Helpers to define models.

Considering:
* have growing entity and entity types, and needs flexable attributes,
* may need to add / delete a kind of attri and related code.
* may need to split some part the database out into another component.

To make it easier to index entities cross app / db / table, use uuid as
key of diffrent type of entities.
Use a namespace uuid (NS) to distinguish between different type of entities.

And to make the integrity easier, split out all the key (NS and UUID) of
diffrent entities into one big table, which also make it more cache friendly.
"""

from .entity import EntityModel
from .attribute import AttributeModel, SharedAttributeModel
from .bare_entity import BareEntityModel

from .utils import _extend_column_arg_patch

_extend_column_arg_patch()

__all__ = ['EntityModel', 'AttributeModel', 'SharedAttributeModel', 'BareEntityModel']
