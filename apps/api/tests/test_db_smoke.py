from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def test_db_session_is_async_session(db_session: AsyncSession):
    assert isinstance(db_session, AsyncSession)


async def test_db_session_executes_query(db_session: AsyncSession):
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


async def test_db_session_rolls_back(db_session: AsyncSession):
    """Verify rollback leaves no residual state (idempotent clean-up)."""
    await db_session.execute(text("SELECT 1"))
    await db_session.rollback()
    # A second query after rollback must still succeed.
    result = await db_session.execute(text("SELECT 2"))
    assert result.scalar() == 2
