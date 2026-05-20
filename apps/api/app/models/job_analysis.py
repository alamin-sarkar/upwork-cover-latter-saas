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
    from app.models.user import User


class JobAnalysisSnapshot(Base):
    __tablename__ = "job_analysis_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    raw_job_text: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(String(240))
    scope: Mapped[str] = mapped_column(Text)
    deliverables: Mapped[list[str]] = mapped_column(JSON, default=list)
    required_skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    budget_clues: Mapped[list[str]] = mapped_column(JSON, default=list)
    urgency: Mapped[str] = mapped_column(String(40))
    tone: Mapped[str] = mapped_column(String(40))
    risk_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    fit_score: Mapped[int] = mapped_column(Integer)
    analysis_payload: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    provider: Mapped[str] = mapped_column(String(40), default="anthropic", server_default="anthropic")
    model_name: Mapped[str] = mapped_column(String(120))
    prompt_version: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship()
