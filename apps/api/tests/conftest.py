import asyncio
import sys

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# psycopg3 async is incompatible with Windows ProactorEventLoop.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.core.config import get_settings


def _async_url(url: str) -> str:
    return url.replace("postgresql+psycopg://", "postgresql+psycopg_async://", 1)


@pytest.fixture
async def db_session() -> AsyncSession:
    settings = get_settings()
    engine = create_async_engine(_async_url(settings.database_url), echo=False)
    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with factory() as session:
        yield session
        await session.rollback()
    await engine.dispose()
