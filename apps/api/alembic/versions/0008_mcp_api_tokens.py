"""phase 10: mcp api tokens

Revision ID: 0008
Revises: 0007
Create Date: 2026-05-20 10:30:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0008"
down_revision: str | None = "0007"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "mcp_api_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("token_prefix", sa.String(length=24), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index(
        op.f("ix_mcp_api_tokens_token_prefix"),
        "mcp_api_tokens",
        ["token_prefix"],
        unique=False,
    )
    op.create_index(
        op.f("ix_mcp_api_tokens_user_id"),
        "mcp_api_tokens",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_mcp_api_tokens_user_id"), table_name="mcp_api_tokens")
    op.drop_index(op.f("ix_mcp_api_tokens_token_prefix"), table_name="mcp_api_tokens")
    op.drop_table("mcp_api_tokens")
