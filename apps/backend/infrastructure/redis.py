from typing import Any

import redis.asyncio as redis
from redis.asyncio import Redis

from core.config import settings


class RedisManager:
    def __init__(self, redis_url: str, prefix: str = "app") -> None:
        self.redis_url = redis_url
        self.prefix = prefix
        self.client: Redis | None = None

    async def connect(self) -> None:
        self.client = redis.from_url(self.redis_url, decode_responses=True)

        await self.client.ping()

    def _get_active_client(self) -> Redis:
        if self.client is None:
            raise RuntimeError("Redis не подключен. Сделайте connect()")

        return self.client

    def _build_key(self, key: str) -> str:
        return f"{self.prefix}:{key}"

    async def exists(self, key: str) -> bool:
        client = self._get_active_client()
        return bool(await client.exists(self._build_key(key)))

    async def expire(self, key: str, seconds: int) -> bool:
        client = self._get_active_client()

        return await client.expire(self._build_key(key), time=seconds)

    async def set(
        self, key: str, value: Any, expire: int | None = None, nx: bool = False
    ) -> bool:  # noqa: E501
        client = self._get_active_client()

        return bool(
            await client.set(name=self._build_key(key), value=value, ex=expire, nx=nx)
        )

    async def get(self, key: str) -> Any:
        client = self._get_active_client()

        return await client.get(name=self._build_key(key))

    async def delete(self, *keys: str) -> int:
        client = self._get_active_client()
        pre_keys = [self._build_key(k) for k in keys]
        return await client.delete(*pre_keys)

    async def close(self) -> None:
        if self.client is not None:
            await self.client.aclose()
            self.client = None


redis_manager = RedisManager(redis_url=settings.REDIS_URL, prefix="app")
