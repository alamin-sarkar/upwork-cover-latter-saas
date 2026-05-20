"""feedback memory and adaptive improvement

Revision ID: 0007
Revises: 0006
Create Date: 2026-05-20 18:45:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cover_letter_feedback",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("generation_run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("generation_variant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("edited_cover_letter", sa.Text(), nullable=True),
        sa.Column("accepted_sections", sa.JSON(), nullable=False),
        sa.Column("rejected_sections", sa.JSON(), nullable=False),
        sa.Column("client_response_outcome", sa.String(length=40), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("memory_text", sa.Text(), nullable=False),
        sa.Column("memory_embedding", Vector(256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("rating >= 1 AND rating <= 5", name="ck_cover_letter_feedback_rating"),
        sa.CheckConstraint(
            "client_response_outcome IN ('no_response', 'replied', 'interview', 'hired', 'rejected')",
            name="ck_cover_letter_feedback_client_response_outcome",
        ),
        sa.ForeignKeyConstraint(["generation_run_id"], ["cover_letter_generation_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["generation_variant_id"],
            ["cover_letter_generation_variants.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("generation_variant_id"),
    )
    op.create_index(
        op.f("ix_cover_letter_feedback_user_id"),
        "cover_letter_feedback",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_cover_letter_feedback_generation_run_id"),
        "cover_letter_feedback",
        ["generation_run_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_cover_letter_feedback_generation_variant_id"),
        "cover_letter_feedback",
        ["generation_variant_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_cover_letter_feedback_generation_variant_id"),
        table_name="cover_letter_feedback",
    )
    op.drop_index(
        op.f("ix_cover_letter_feedback_generation_run_id"),
        table_name="cover_letter_feedback",
    )
    op.drop_index(op.f("ix_cover_letter_feedback_user_id"), table_name="cover_letter_feedback")
    op.drop_table("cover_letter_feedback")
