"""cover letter library domain

Revision ID: 0004
Revises: 0003
Create Date: 2026-05-20 12:10:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cover_letter_guidelines",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("guideline_type", sa.String(length=40), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "guideline_type IN ('rule', 'intro', 'cta', 'tone_preset')",
            name="ck_cover_letter_guidelines_guideline_type",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_cover_letter_guidelines_guideline_type"),
        "cover_letter_guidelines",
        ["guideline_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_cover_letter_guidelines_user_id"),
        "cover_letter_guidelines",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "cover_letter_samples",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("tag", sa.String(length=40), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("outcome", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "tag IN ('winning', 'anti-pattern')",
            name="ck_cover_letter_samples_tag",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cover_letter_samples_tag"), "cover_letter_samples", ["tag"], unique=False)
    op.create_index(
        op.f("ix_cover_letter_samples_user_id"),
        "cover_letter_samples",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_cover_letter_samples_user_id"), table_name="cover_letter_samples")
    op.drop_index(op.f("ix_cover_letter_samples_tag"), table_name="cover_letter_samples")
    op.drop_table("cover_letter_samples")

    op.drop_index(
        op.f("ix_cover_letter_guidelines_user_id"),
        table_name="cover_letter_guidelines",
    )
    op.drop_index(
        op.f("ix_cover_letter_guidelines_guideline_type"),
        table_name="cover_letter_guidelines",
    )
    op.drop_table("cover_letter_guidelines")
