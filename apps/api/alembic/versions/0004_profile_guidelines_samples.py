"""add profile guidelines and samples

Revision ID: 0004_profile_guidelines_samples
Revises: 0003_profile_projects_professional_custom_sections
Create Date: 2026-05-19
"""

from alembic import op
import sqlalchemy as sa


revision = "0004_profile_guidelines_samples"
down_revision = "0003_profile_projects_professional_custom_sections"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "profile_guidelines",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("profile_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("content", sa.String(length=5000), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "profile_samples",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("profile_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("body", sa.String(length=7000), nullable=False),
        sa.Column("tone", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("profile_samples")
    op.drop_table("profile_guidelines")
