"""add job analysis snapshot fields

Revision ID: 0007_job_analysis_snapshot
Revises: 0006_cover_letter_feedback_memory
Create Date: 2026-05-19
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0007_job_analysis_snapshot"
down_revision = "0006_cover_letter_feedback_memory"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("cover_letter_job_posts", sa.Column("analysis_snapshot", sa.JSON(), nullable=True))
    op.add_column("cover_letter_job_posts", sa.Column("fit_score", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("cover_letter_job_posts", "fit_score")
    op.drop_column("cover_letter_job_posts", "analysis_snapshot")
