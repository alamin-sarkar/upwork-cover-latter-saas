"""add users table

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-19

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# PostgreSQL-specific ENUM with create_type=False so op.create_table doesn't
# try to CREATE TYPE again after we've already done it explicitly below.
_plan_enum = PgEnum("free", "pro", "team", name="plan", create_type=False)


def upgrade() -> None:
    # Create enum type first (idempotent via DO block).
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE plan AS ENUM ('free', 'pro', 'team');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
    """)

    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("hashed_password", sa.String(100), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=True),
        sa.Column("plan", _plan_enum, nullable=False, server_default="free"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS plan")
