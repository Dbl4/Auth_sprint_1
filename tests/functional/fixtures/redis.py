import pytest_asyncio
from redis import asyncio as aioredis

from tests.functional.settings import test_settings


@pytest_asyncio.fixture(scope="session")
async def redis_client():
    client = await aioredis.from_url(
        test_settings.redis_dsn,
        encoding="utf-8",
        decode_responses=True,
    )
    yield client
    await client.flushall()
    await client.close()
