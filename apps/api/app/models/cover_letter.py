import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class CoverLetterJobPost(Base):
    __tablename__ = "cover_letter_job_posts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    source: Mapped[str] = mapped_column(String(40), nullable=False, default="upwork")
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CoverLetterGeneration(Base):
    __tablename__ = "cover_letter_generations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cover_letter_job_posts.id", ondelete="CASCADE"), nullable=False)
    structure: Mapped[str] = mapped_column(String(80), nullable=False)
    analysis_summary: Mapped[str] = mapped_column(Text, nullable=False)
    draft_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    job_post: Mapped[CoverLetterJobPost] = relationship()
