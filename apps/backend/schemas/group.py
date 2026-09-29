from datetime import datetime

from pydantic import Field, HttpUrl

from schemas.base import BaseModelConf, GroupStatus, MemberRole, SkillLevel
from schemas.user import UserProfileResponse


class GroupMemberResponse(BaseModelConf):
    user: UserProfileResponse
    role: MemberRole
    joined_at: datetime

class GroupBase(BaseModelConf):
    name: str = Field(min_length=2, max_length=100)
    industry: str = Field(min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=1000)
    level: SkillLevel
    chat_links: list[str] = Field(default_factory=list)
    repo_links: list[str] | None = Field(default_factory=list)

class GroupCreate(GroupBase):
    max_member: int = Field(default=5, ge=2, le=5)
    roadmap_id: int | None = None

class GroupUpdate(BaseModelConf):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    industry: str | None = None
    description: str | None = None
    level: SkillLevel | None = None
    chat_links: list[str] | None = None
    repo_links: list[str] | None = None
    max_capacity: int | None = Field(default=None, ge=2, le=5)
    status: GroupStatus | None = None

class GroupResponse(GroupBase):
    id: int
    captain_id: int
    status: GroupStatus
    max_capacity: int
    members_count: int
    members: list[GroupMemberResponse] = Field(default_factory=list)
    created_at: datetime


class GroupFilterParams(BaseModelConf):
    industry: str | None = None
    level: SkillLevel | None = None
    search: str | None = None
    is_recruiting: bool | None = None
