from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings


def _async_url(url: str) -> str:
    """Rewrite psycopg3 sync driver to async driver for SQLAlchemy."""
    return url.replace("postgresql+psycopg://", "postgresql+psycopg_async://", 1)


def _build_engine():
    settings = get_settings()
    return create_async_engine(
        _async_url(settings.database_url),
        echo=settings.environment == "development",
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


engine = _build_engine()

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
