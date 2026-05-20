"""cover letter generation history

Revision ID: 0006
Revises: 0005
Create Date: 2026-05-20 15:35:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cover_letter_generation_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("analysis_snapshot_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("raw_job_text", sa.Text(), nullable=False),
        sa.Column("requested_structures", sa.JSON(), nullable=False),
        sa.Column("prompt_version", sa.String(length=80), nullable=False),
        sa.Column("graph_state", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_snapshot_id"], ["job_analysis_snapshots.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_cover_letter_generation_runs_analysis_snapshot_id"),
        "cover_letter_generation_runs",
        ["analysis_snapshot_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_cover_letter_generation_runs_user_id"),
        "cover_letter_generation_runs",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "cover_letter_generation_variants",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("generation_run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("structure", sa.String(length=40), nullable=False),
        sa.Column("headline", sa.String(length=160), nullable=False),
        sa.Column("cover_letter", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("match_notes", sa.JSON(), nullable=False),
        sa.Column("self_check_notes", sa.JSON(), nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "structure IN ('concise', 'problem-solution', 'credibility-first', 'portfolio-first', 'consultative')",
            name="ck_cover_letter_generation_variants_structure",
        ),
        sa.ForeignKeyConstraint(
            ["generation_run_id"],
            ["cover_letter_generation_runs.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_cover_letter_generation_variants_generation_run_id"),
        "cover_letter_generation_variants",
        ["generation_run_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_cover_letter_generation_variants_generation_run_id"),
        table_name="cover_letter_generation_variants",
    )
    op.drop_table("cover_letter_generation_variants")

    op.drop_index(
        op.f("ix_cover_letter_generation_runs_user_id"),
        table_name="cover_letter_generation_runs",
    )
    op.drop_index(
        op.f("ix_cover_letter_generation_runs_analysis_snapshot_id"),
        table_name="cover_letter_generation_runs",
    )
    op.drop_table("cover_letter_generation_runs")
