from typing import overload

from metadash.models.base import EntityModel  # Skeleton / Tmp WIP
from sqlalchemy import event


METADASH_TO_SQLALCHEMY_EVNET_MAP = {
    'after_save': ['after_update', 'after_insert'],
    'before_save': ['before_update', 'before_insert']
}

SQLALCHEMY_MAPPER_EVENTS = [
    # 'after_configured',
    'after_delete',
    'after_insert',
    'after_update',
    # 'before_configured',
    'before_delete',
    'before_insert',
    'before_update',
    # 'instrument_class',
    # 'mapper_configured',
    '']


def on(entity: EntityModel, event_name):
    """
    Only works for SQLAlchemy Mapper based entity
    listener function should be like:
    def listen(mapper, connection, target):
        pass
    """
    def wa(f):
        if event_name in SQLALCHEMY_MAPPER_EVENTS:
            event.listens_for(entity, event_name)(f)
        elif event_name in METADASH_TO_SQLALCHEMY_EVNET_MAP:
            events = METADASH_TO_SQLALCHEMY_EVNET_MAP[event_name]
            if isinstance(events, list):
                for ev in events:
                    event.listens_for(entity, ev)(f)
            elif isinstance(events, str):
                event.listens_for(entity, events)(f)
        return f
    return wa
