from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database import Base
from models.base import enum_column
from schemas.base import GroupStatus, MemberRole, SkillLevel

if TYPE_CHECKING:
    from models.competition import Competition
    from models.event import CalendarEvent
    from models.project import Project
    from models.roadmap import Roadmap, TopicProgress
    from models.user import User


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    industry: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    level: Mapped[SkillLevel] = mapped_column(
        enum_column(SkillLevel, "group_level_enum"),
        nullable=False,
    )

    chat_links: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    repo_links: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    max_capacity: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    status: Mapped[GroupStatus] = mapped_column(
        enum_column(GroupStatus, "group_status_enum"),
        default=GroupStatus.ACTIVE,
        nullable=False,
    )

    captain_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    roadmap_id: Mapped[int | None] = mapped_column(
        ForeignKey("roadmaps.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    captain: Mapped[User] = relationship(
        back_populates="captain_groups",
        foreign_keys=[captain_id],
    )

    roadmap: Mapped[Roadmap | None] = relationship(
        back_populates="groups",
    )

    members: Mapped[list[GroupMember]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
    )

    events: Mapped[list[CalendarEvent]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
    )

    projects: Mapped[list[Project]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
    )

    competitions: Mapped[list[Competition]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
    )

    topic_progress: Mapped[list[TopicProgress]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
    )

    @property
    def members_count(self) -> int:
        if "members" in self.__dict__ and self.members is not None:
            return len(self.members)
        return 0


class GroupMember(Base):
    __tablename__ = "group_members"
    __table_args__ = (
        UniqueConstraint("group_id", "user_id", name="uq_group_members_group_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[MemberRole] = mapped_column(
        enum_column(MemberRole, "member_role_enum"),
        default=MemberRole.MEMBER,
        nullable=False,
    )

    joined_at: Mapped[datetime] = mapped_column(server_default=func.now())

    group: Mapped[Group] = relationship(back_populates="members")
    user: Mapped[User] = relationship(back_populates="memberships")
