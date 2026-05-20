"""job analysis snapshots

Revision ID: 0005
Revises: 0004
Create Date: 2026-05-20 14:35:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0005"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "job_analysis_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("raw_job_text", sa.Text(), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("scope", sa.Text(), nullable=False),
        sa.Column("deliverables", sa.JSON(), nullable=False),
        sa.Column("required_skills", sa.JSON(), nullable=False),
        sa.Column("budget_clues", sa.JSON(), nullable=False),
        sa.Column("urgency", sa.String(length=40), nullable=False),
        sa.Column("tone", sa.String(length=40), nullable=False),
        sa.Column("risk_flags", sa.JSON(), nullable=False),
        sa.Column("fit_score", sa.Integer(), nullable=False),
        sa.Column("analysis_payload", sa.JSON(), nullable=False),
        sa.Column("provider", sa.String(length=40), server_default="anthropic", nullable=False),
        sa.Column("model_name", sa.String(length=120), nullable=False),
        sa.Column("prompt_version", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("fit_score >= 0 AND fit_score <= 100", name="ck_job_analysis_fit_score"),
        sa.CheckConstraint("urgency IN ('low', 'medium', 'high')", name="ck_job_analysis_urgency"),
        sa.CheckConstraint(
            "tone IN ('formal', 'neutral', 'friendly', 'demanding')",
            name="ck_job_analysis_tone",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_job_analysis_snapshots_user_id"),
        "job_analysis_snapshots",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_job_analysis_snapshots_user_id"), table_name="job_analysis_snapshots")
    op.drop_table("job_analysis_snapshots")
