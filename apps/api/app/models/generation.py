from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.job_analysis import JobAnalysisSnapshot
    from app.models.user import User


class CoverLetterGenerationRun(Base):
    __tablename__ = "cover_letter_generation_runs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    analysis_snapshot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job_analysis_snapshots.id", ondelete="CASCADE"),
        index=True,
    )
    raw_job_text: Mapped[str] = mapped_column(Text)
    requested_structures: Mapped[list[str]] = mapped_column(JSON, default=list)
    prompt_version: Mapped[str] = mapped_column(String(80))
    graph_state: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship()
    analysis_snapshot: Mapped["JobAnalysisSnapshot"] = relationship()
    variants: Mapped[list["CoverLetterGenerationVariant"]] = relationship(
        back_populates="generation_run",
        cascade="all, delete-orphan",
        order_by="CoverLetterGenerationVariant.sort_order",
    )


class CoverLetterGenerationVariant(Base):
    __tablename__ = "cover_letter_generation_variants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    generation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cover_letter_generation_runs.id", ondelete="CASCADE"),
        index=True,
    )
    structure: Mapped[str] = mapped_column(String(40))
    headline: Mapped[str] = mapped_column(String(160))
    cover_letter: Mapped[str] = mapped_column(Text)
    rationale: Mapped[str] = mapped_column(Text)
    match_notes: Mapped[list[str]] = mapped_column(JSON, default=list)
    self_check_notes: Mapped[list[str]] = mapped_column(JSON, default=list)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    generation_run: Mapped["CoverLetterGenerationRun"] = relationship(back_populates="variants")
