from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.generation import CoverLetterGenerationRun, CoverLetterGenerationVariant
    from app.models.user import User


FEEDBACK_EMBEDDING_DIMENSIONS = 256


class CoverLetterFeedback(Base):
    __tablename__ = "cover_letter_feedback"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    generation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cover_letter_generation_runs.id", ondelete="CASCADE"),
        index=True,
    )
    generation_variant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cover_letter_generation_variants.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    rating: Mapped[int] = mapped_column(Integer)
    edited_cover_letter: Mapped[str | None] = mapped_column(Text, nullable=True)
    accepted_sections: Mapped[list[str]] = mapped_column(JSON, default=list)
    rejected_sections: Mapped[list[str]] = mapped_column(JSON, default=list)
    client_response_outcome: Mapped[str] = mapped_column(String(40))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    memory_text: Mapped[str] = mapped_column(Text)
    memory_embedding: Mapped[list[float]] = mapped_column(Vector(FEEDBACK_EMBEDDING_DIMENSIONS))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship()
    generation_run: Mapped["CoverLetterGenerationRun"] = relationship()
    generation_variant: Mapped["CoverLetterGenerationVariant"] = relationship()
