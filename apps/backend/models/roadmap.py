from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database import Base
from models.base import enum_column
from schemas.base import ResourceType

if TYPE_CHECKING:
    from models.group import Group
    from models.user import User


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    groups: Mapped[list[Group]] = relationship(back_populates="roadmap")

    topics: Mapped[list[RoadmapTopic]] = relationship(
        back_populates="roadmap",
        cascade="all, delete-orphan",
        order_by="RoadmapTopic.order",
    )


class RoadmapTopic(Base):
    __tablename__ = "roadmap_topics"

    id: Mapped[int] = mapped_column(primary_key=True)

    roadmap_id: Mapped[int] = mapped_column(
        ForeignKey("roadmaps.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    roadmap: Mapped[Roadmap] = relationship(back_populates="topics")

    resources: Mapped[list[Resource]] = relationship(
        back_populates="topic",
        cascade="all, delete-orphan",
    )

    progress: Mapped[list[TopicProgress]] = relationship(
        back_populates="topic",
        cascade="all, delete-orphan",
    )


class Resource(Base):
    __tablename__ = "roadmap_resources"

    id: Mapped[int] = mapped_column(primary_key=True)

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("roadmap_topics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)

    resource_type: Mapped[ResourceType] = mapped_column(
        enum_column(ResourceType, "resource_type_enum"),
        default=ResourceType.ARTICLE,
        nullable=False,
    )

    topic: Mapped[RoadmapTopic] = relationship(back_populates="resources")


class TopicProgress(Base):
    __tablename__ = "topic_progress"
    __table_args__ = (
        UniqueConstraint(
            "group_id",
            "topic_id",
            "user_id",
            name="uq_topic_progress_group_topic_user",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("roadmap_topics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    group: Mapped[Group] = relationship(back_populates="topic_progress")
    topic: Mapped[RoadmapTopic] = relationship(back_populates="progress")
    user: Mapped[User] = relationship(back_populates="topic_progress")
