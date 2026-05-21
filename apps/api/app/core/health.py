from __future__ import annotations

import asyncio
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.db import SessionLocal
from app.core.redis import get_redis_client
from app.worker import celery_app


async def check_database() -> dict[str, Any]:
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"ok": True}
    except SQLAlchemyError as exc:
        return {"ok": False, "detail": str(exc)}


async def check_redis() -> dict[str, Any]:
    try:
        return {"ok": bool(await get_redis_client().ping())}
    except Exception as exc:  # pragma: no cover - runtime dependent
        return {"ok": False, "detail": str(exc)}


async def check_celery_workers() -> dict[str, Any]:
    try:
        result = await asyncio.to_thread(lambda: celery_app.control.inspect(timeout=1).ping())
        return {"ok": bool(result), "workers": result or {}}
    except Exception as exc:  # pragma: no cover - runtime dependent
        return {"ok": False, "detail": str(exc)}
