from datetime import datetime

from pydantic import Field, field_validator

from schemas.base import BaseModelConf, SkillLevel


class UserProfileBase(BaseModelConf):
    name: str = Field(min_length=2, max_length=50)
    username: str = Field(min_length=3, max_length=30)
    bio: str | None = Field(default=None, max_length=500)
    skill_level: SkillLevel
    interests: list[str] = Field(default_factory=list)

    @field_validator("interests")
    @classmethod
    def clean_interest(cls, tags: list[str]) -> list[str]:
        return [t.strip().lower() for t in tags if t.strip()]


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModelConf):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    username: str | None = Field(default=None, min_length=3, max_length=30)
    bio: str | None = Field(default=None, max_length=500)
    skill_level: SkillLevel | None = None
    interests: list[str] | None = None

    @field_validator("interests")
    @classmethod
    def clean_interest(cls, tags: list[str] | None) -> list[str] | None:
        if tags is None:
            return None
        return [t.strip().lower() for t in tags if t.strip()]


class UserProfileResponse(UserProfileBase):
    id: int
    created_at: datetime
