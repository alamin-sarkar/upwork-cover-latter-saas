from redis.asyncio import Redis

from app.core.config import get_settings


def get_redis_client() -> Redis:
    settings = get_settings()
    return Redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)


async def close_redis_client() -> None:
    return None
