from datetime import datetime

from pydantic import Field

from schemas.base import BaseModelConf


class CalendarEventBase(BaseModelConf):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None
    start_time: datetime
    end_time: datetime
    tags: list[str] = Field(
        default_factory=list, description="Теги: созвон, дедлайн, чекпоинт"
    )


class CalendarEventCreate(CalendarEventBase):
    group_id: int


class CalendarEventUpdate(BaseModelConf):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    tags: list[str] | None = None


class CalendarEventResponse(CalendarEventBase):
    id: int
    group_id: int
    creator_id: int
