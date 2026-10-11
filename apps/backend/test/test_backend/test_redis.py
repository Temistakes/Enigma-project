import pytest

from core.config import settings
from infrastructure.redis import RedisManager


def test_settings_mode() -> None:
    assert settings.MODE == "TEST"


async def test_not_connected_raises_error() -> None:
    manager = RedisManager(redis_url=settings.REDIS_URL, prefix="test")
    with pytest.raises(RuntimeError, match="Redis не подключен"):
        await manager.get("any_key")


async def test_repeated_connect_safe(redis_test: RedisManager) -> None:
    await redis_test.connect()
    assert redis_test.client is not None


async def test_set_and_get(redis_test: RedisManager) -> None:
    key = "user_status"
    value = "active"

    assert await redis_test.set(key, value) is True
    assert await redis_test.get(key) == value


async def test_prefix_isolation(redis_test: RedisManager) -> None:
    key = "test_code"
    await redis_test.set(key, "12345")

    client = redis_test._get_active_client()
    exists = await client.exists(f"{redis_test.prefix}:{key}")
    assert exists == 1


async def test_exists_and_delete(redis_test: RedisManager) -> None:
    key = "cache_item"
    await redis_test.set(key, "data")

    assert await redis_test.exists(key) is True
    assert await redis_test.delete(key) == 1
    assert await redis_test.exists(key) is False


async def test_expire_ttl(redis_test: RedisManager) -> None:
    key = "token"
    await redis_test.set(key, "data")

    assert await redis_test.expire(key, seconds=30) is True

    client = redis_test._get_active_client()
    ttl = await client.ttl(redis_test._build_key(key))
    assert 0 < ttl <= 30
