"""
Redis connection and utilities.
"""
import redis.asyncio as aioredis
from typing import Optional

from app.core.config import get_settings

settings = get_settings()

# Redis connection pool
redis_pool = aioredis.ConnectionPool.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
)


async def get_redis() -> aioredis.Redis:
    """Get Redis connection."""
    return aioredis.Redis(connection_pool=redis_pool)


async def redis_set(key: str, value: str, expire: Optional[int] = None) -> bool:
    """Set a key-value pair in Redis."""
    r = await get_redis()
    return await r.set(key, value, ex=expire)


async def redis_get(key: str) -> Optional[str]:
    """Get a value from Redis."""
    r = await get_redis()
    return await r.get(key)


async def redis_delete(key: str) -> int:
    """Delete a key from Redis."""
    r = await get_redis()
    return await r.delete(key)


async def redis_exists(key: str) -> bool:
    """Check if a key exists in Redis."""
    r = await get_redis()
    return await r.exists(key) > 0
