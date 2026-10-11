import os
from collections.abc import AsyncGenerator

import pytest

os.environ["MODE"] = "TEST"

from core.config import settings
from infrastructure.redis import RedisManager


@pytest.fixture
async def redis_test() -> AsyncGenerator[RedisManager]:
    manager = RedisManager(redis_url=settings.REDIS_URL, prefix="test")
    await manager.connect()

    yield manager

    client = manager._get_active_client()
    keys = await client.keys("test:*")
    if keys:
        await client.delete(*keys)
    await manager.close()
