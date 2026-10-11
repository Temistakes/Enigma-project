from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database import Base
from models.base import enum_column
from schemas.base import SkillLevel

if TYPE_CHECKING:
    from models.competition import Competition, CompetitionParticipant
    from models.event import CalendarEvent
    from models.group import Group, GroupMember
    from models.project import Project, ProjectTask
    from models.roadmap import TopicProgress


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    bio: Mapped[str | None] = mapped_column(String(500), nullable=True)

    skill_level: Mapped[SkillLevel] = mapped_column(
        enum_column(SkillLevel, "skill_level_enum"),
        default=SkillLevel.BEGINNER,
        nullable=False,
    )

    interests: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    memberships: Mapped[list[GroupMember]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    captain_groups: Mapped[list[Group]] = relationship(
        back_populates="captain",
        foreign_keys="Group.captain_id",
    )

    created_events: Mapped[list[CalendarEvent]] = relationship(
        back_populates="creator",
        foreign_keys="CalendarEvent.creator_id",
    )

    topic_progress: Mapped[list[TopicProgress]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    owned_projects: Mapped[list[Project]] = relationship(
        back_populates="creator",
        foreign_keys="Project.creator_id",
    )

    assigned_tasks: Mapped[list[ProjectTask]] = relationship(
        back_populates="assignee",
        foreign_keys="ProjectTask.assignee_id",
    )

    created_competitions: Mapped[list[Competition]] = relationship(
        back_populates="creator",
        foreign_keys="Competition.creator_id",
    )

    competition_participations: Mapped[list[CompetitionParticipant]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
