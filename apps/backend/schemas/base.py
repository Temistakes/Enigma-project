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


class ProjectStatus(StrEnum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class CompetitionStatus(StrEnum):
    PLANNED = "planned"
    ACTIVE = "active"
    FINISHED = "finished"
    CANCELLED = "cancelled"
