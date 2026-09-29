from datetime import datetime

from pydantic import Field, HttpUrl, computed_field

from schemas.base import BaseModelConf, ResourceType


class ResourceItem(BaseModelConf):
    title: str = Field(min_length=1, max_length=150)
    url: HttpUrl
    resource_type: ResourceType = ResourceType.ARTICLE


class RoadmapTopicBase(BaseModelConf):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None
    order: int = Field(
        default=1, ge=1, description="Порядковый номер тем. Потом забуду просто"
    )
    resource: list[ResourceItem] = Field(default_factory=list)


class RoadmapTopicCreate(RoadmapTopicBase):
    pass


class RoadmapTopicResponse(RoadmapTopicBase):
    id: int


class ToggleTopicProgressRequest(BaseModelConf):
    topic_id: int
    is_completed: bool


class ParticipantProgressItem(BaseModelConf):
    user_id: int
    is_completed: bool
    completed_at: datetime | None = None


class GroupTopicProgressResponse(BaseModelConf):
    topic: RoadmapTopicResponse
    participants_progress: list[ParticipantProgressItem] = Field(default_factory=list)

    @computed_field
    @property
    def is_team_completed(self) -> bool:
        if not self.participants_progress:
            return False
        return all(p.is_completed for p in self.participants_progress)
