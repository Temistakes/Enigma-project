from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class BaseModelConf(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SkillLevel(StrEnum):
    BEGINNER = "beginner"
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"


class GroupStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"


class MemberRole(StrEnum):
    CAPTAIN = "captain"
    MEMBER = "member"


class ResourceType(StrEnum):
    ARTICLE = "article"
    VIDEO = "video"
    BOOK = "book"
    DOCS = "docs"
