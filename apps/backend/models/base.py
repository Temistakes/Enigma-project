from __future__ import annotations

from enum import Enum

from sqlalchemy import Enum as SAEnum


def enum_column(enum_cls: type[Enum], name: str) -> SAEnum:
    """
    Единый способ хранить StrEnum в БД как VARCHAR.
    """
    return SAEnum(
        enum_cls,
        native_enum=False,
        values_callable=lambda enum: [item.value for item in enum],
        name=name,
        length=50,
    )
