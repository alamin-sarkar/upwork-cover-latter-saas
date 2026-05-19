from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0003_profile_projects_professional_custom_sections"
down_revision = "0002_profile_and_skills"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "profile_projects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("profile_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=3000), nullable=True),
        sa.Column("tech_stack", sa.String(length=500), nullable=True),
        sa.Column("impact", sa.String(length=500), nullable=True),
        sa.Column("project_url", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "profile_professional_life",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("profile_id", sa.Uuid(), nullable=False),
        sa.Column("company", sa.String(length=200), nullable=False),
        sa.Column("role_title", sa.String(length=200), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("summary", sa.String(length=3000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "profile_custom_sections",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("profile_id", sa.Uuid(), nullable=False),
        sa.Column("section_name", sa.String(length=120), nullable=False),
        sa.Column("content", sa.String(length=5000), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("profile_custom_sections")
    op.drop_table("profile_professional_life")
    op.drop_table("profile_projects")
