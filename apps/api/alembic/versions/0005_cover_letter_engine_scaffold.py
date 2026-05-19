"""add cover letter engine scaffold tables

Revision ID: 0005_cover_letter_engine_scaffold
Revises: 0004_profile_guidelines_samples
Create Date: 2026-05-19
"""

from alembic import op
import sqlalchemy as sa


revision = "0005_cover_letter_engine_scaffold"
down_revision = "0004_profile_guidelines_samples"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cover_letter_job_posts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("source", sa.String(length=40), nullable=False),
        sa.Column("title", sa.String(length=300), nullable=False),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "cover_letter_generations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("job_post_id", sa.Uuid(), nullable=False),
        sa.Column("structure", sa.String(length=80), nullable=False),
        sa.Column("analysis_summary", sa.Text(), nullable=False),
        sa.Column("draft_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["job_post_id"], ["cover_letter_job_posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("cover_letter_generations")
    op.drop_table("cover_letter_job_posts")
