from datetime import datetime

from sqlalchemy import JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database import Base
from schemas.base import SkillLevel
from schemas.group import GroupMemberResponse


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    bio: Mapped[str | None] = mapped_column(String(500), nullable=True)
    skill_level: Mapped[SkillLevel] = mapped_column(default=SkillLevel.BEGINNER)

    interests: Mapped[list[str]] = mapped_column(JSON, default=list)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    memberships: Mapped[list["GroupMemberResponse"]] = relationship(
        back_populates="user"
    )
