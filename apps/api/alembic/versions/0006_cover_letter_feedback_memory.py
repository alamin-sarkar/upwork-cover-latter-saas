"""add cover letter feedback memory

Revision ID: 0006_cover_letter_feedback_memory
Revises: 0005_cover_letter_engine_scaffold
Create Date: 2026-05-19
"""

from alembic import op
import sqlalchemy as sa


revision = "0006_cover_letter_feedback_memory"
down_revision = "0005_cover_letter_engine_scaffold"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cover_letter_feedback",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("generation_id", sa.Uuid(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("feedback_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["generation_id"], ["cover_letter_generations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("cover_letter_feedback")
