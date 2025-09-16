from typing import Any, Optional, Tuple

import redis.asyncio as redis  # Changed from aioredis
from fastapi_cache.backends import Backend  # type: ignore


class RedisBackend(Backend):
    def __init__(self, redis_client: redis.Redis):  # Changed parameter name for clarity
        self.redis = redis_client

    async def get_with_ttl(self, key: str) -> Tuple[int, Optional[Any]]:
        # redis-py async pipeline doesn't use context manager
        pipe = self.redis.pipeline(transaction=True)
        pipe.ttl(key)
        pipe.get(key)
        results = await pipe.execute()
        ttl, value = results[0], results[1]
        return ttl, value

    async def get(self, key: str) -> Optional[Any]:
        return await self.redis.get(key)

    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        return await self.redis.set(key, value, ex=expire)

    async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
        if namespace:
            # Use SCAN instead of KEYS for better performance in production
            pattern = f"{namespace}:*"
            keys = []
            async for key_name in self.redis.scan_iter(match=pattern):
                keys.append(key_name)

            if keys:
                return await self.redis.delete(*keys)
            return 0
        elif key:
            return await self.redis.delete(key)
        return 0
