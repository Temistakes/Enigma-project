from datetime import datetime

from pydantic import Field

from schemas.base import BaseModelConf, CompetitionStatus


class CompetitionParticipantBase(BaseModelConf):
    place: int | None = None
    result: str | None = None


class CompetitionParticipantCreate(CompetitionParticipantBase):
    competition_id: int
    user_id: int


class CompetitionParticipantResponse(CompetitionParticipantBase):
    id: int
    competition_id: int
    user_id: int
    created_at: datetime


class CompetitionBase(BaseModelConf):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None
    start_time: datetime
    end_time: datetime
    status: CompetitionStatus = CompetitionStatus.PLANNED
    result: str | None = None


class CompetitionCreate(CompetitionBase):
    group_id: int | None = None


class CompetitionUpdate(BaseModelConf):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: CompetitionStatus | None = None
    result: str | None = None


class CompetitionResponse(CompetitionBase):
    id: int
    group_id: int | None = None
    creator_id: int
    created_at: datetime
    participants: list[CompetitionParticipantResponse] = Field(default_factory=list)
