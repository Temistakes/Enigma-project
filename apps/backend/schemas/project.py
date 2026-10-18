from datetime import datetime

from pydantic import Field

from schemas.base import BaseModelConf, ProjectStatus, TaskStatus


class ProjectTaskBase(BaseModelConf):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    due_date: datetime | None = None


class ProjectTaskCreate(ProjectTaskBase):
    project_id: int
    assignee_id: int | None = None


class ProjectTaskUpdate(BaseModelConf):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    status: TaskStatus | None = None
    assignee_id: int | None = None
    due_date: datetime | None = None


class ProjectTaskResponse(ProjectTaskBase):
    id: int
    project_id: int
    assignee_id: int | None = None
    created_at: datetime


class ProjectBase(BaseModelConf):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None
    repo_url: str | None = Field(default=None, max_length=500)
    demo_url: str | None = Field(default=None, max_length=500)
    status: ProjectStatus = ProjectStatus.PLANNING


class ProjectCreate(ProjectBase):
    group_id: int


class ProjectUpdate(BaseModelConf):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    repo_url: str | None = Field(default=None, max_length=500)
    demo_url: str | None = Field(default=None, max_length=500)
    status: ProjectStatus | None = None


class ProjectResponse(ProjectBase):
    id: int
    group_id: int
    creator_id: int
    created_at: datetime
    tasks: list[ProjectTaskResponse] = Field(default_factory=list)
