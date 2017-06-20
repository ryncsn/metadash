import uuid

from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as postgre_UUID


# pylint: disable=no-member
class UUID(TypeDecorator):
    """
    Add a native UUID type for sqlalchemy.

    Copy & Pasted from http://docs.sqlalchemy.org/en/latest/core/custom_types.html
    Platform-independent UUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    With PostgreSQL's UUID type, we don't need any special opeartion to create index,
    b-tree index is good enough and hash index is actually worse due to historical problem.
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
        return uuid.UUID(value) if value is not None else None

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)
