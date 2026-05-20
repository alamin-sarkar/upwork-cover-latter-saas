from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum

import structlog
from fastapi import HTTPException, Response, status
from redis.exceptions import RedisError

from app.core.config import get_settings
from app.core.redis import get_redis_client
from app.models.user import User

logger = structlog.get_logger("app.rate_limit")


class RateLimitAction(StrEnum):
    job_analysis = "job_analysis"
    generation = "generation"


@dataclass(slots=True)
class RateLimitResult:
    limit: int
    used: int
    remaining: int
    reset_at: datetime


class InMemoryRateLimitStorage:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._store: dict[str, tuple[int, datetime]] = {}

    async def increment(self, key: str, *, expires_at: datetime) -> int:
        async with self._lock:
            now = datetime.now(UTC)
            current = self._store.get(key)
            if current is None or current[1] <= now:
                self._store[key] = (1, expires_at)
                return 1

            count, current_expiry = current
            self._store[key] = (count + 1, current_expiry)
            return count + 1


_memory_storage = InMemoryRateLimitStorage()


def _window_reset_at() -> datetime:
    now = datetime.now(UTC)
    return (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)


async def _increment_counter(key: str, *, expires_at: datetime) -> int:
    try:
        client = get_redis_client()
        count = await client.incr(key)
        if count == 1:
            ttl_seconds = max(int((expires_at - datetime.now(UTC)).total_seconds()), 1)
            await client.expire(key, ttl_seconds)
        return int(count)
    except (RedisError, RuntimeError, OSError) as exc:
        get_redis_client.cache_clear()
        logger.warning("rate_limit.redis_unavailable", error=str(exc))
        return await _memory_storage.increment(key, expires_at=expires_at)


async def enforce_rate_limit(
    *,
    user: User,
    action: RateLimitAction,
    response: Response | None = None,
) -> RateLimitResult:
    settings = get_settings()
    reset_at = _window_reset_at()
    if action is RateLimitAction.job_analysis:
        limit = settings.plan_limit_for(settings.job_analysis_daily_limits, user.plan)
    else:
        limit = settings.plan_limit_for(settings.generation_daily_limits, user.plan)

    key = f"rate-limit:{action.value}:{user.id}:{reset_at.date().isoformat()}"
    used = await _increment_counter(key, expires_at=reset_at)
    remaining = max(limit - used, 0)

    if response is not None:
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = reset_at.isoformat()
        response.headers["X-RateLimit-Action"] = action.value

    if used > limit:
        logger.info(
            "rate_limit.exceeded",
            user_id=str(user.id),
            action=action.value,
            plan=user.plan.value,
            limit=limit,
            used=used,
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Daily {action.value.replace('_', ' ')} limit reached for plan {user.plan.value}",
        )

    return RateLimitResult(limit=limit, used=used, remaining=remaining, reset_at=reset_at)
