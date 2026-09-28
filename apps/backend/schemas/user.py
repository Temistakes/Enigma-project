from datetime import datetime

from pydantic import Field

from schemas.common import BaseModelConf, SkillLevel


class UserProfileBase(BaseModelConf):
    name: str = Field(min_length=2, max_length=50)
    username: str = Field(min_length=3, max_length=30)
    bio: str | None = Field(default=None, max_length=500)
    skill_level: SkillLevel
    interests: list[str] = []


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModelConf):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    username: str | None = Field(default=None, min_length=3, max_length=30)
    bio: str | None = Field(default=None, max_length=500)
    skill_level: SkillLevel | None = None
    interests: list[str] | None = None


class UserProfileResponse(UserProfileBase):
    id: int
    created_at: datetime
