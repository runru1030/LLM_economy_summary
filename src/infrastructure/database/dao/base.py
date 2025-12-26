from datetime import UTC
from sqlalchemy import TIMESTAMP, TypeDecorator
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class UTCTimestamp(TypeDecorator):
    impl = TIMESTAMP
    cache_ok = True

    def process_bind_param(self, value, _):
        if value is not None:
            if not value.tzinfo:
                raise TypeError("tzinfo is required")
            value = value.astimezone(UTC).replace(tzinfo=None)
        return value

    def process_result_value(self, value, _):
        if value is not None:
            value = value.replace(tzinfo=UTC)
        return value
