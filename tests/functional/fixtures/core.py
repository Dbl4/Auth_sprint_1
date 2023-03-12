import asyncio

import pytest
import pytest_asyncio


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def cleanup(redis_client, es_client):
    await redis_client.flushall()
    await es_client.delete_by_query(
        index=["movies", "genres", "persons"],
        body={"query": {"match_all": {}}},
        conflicts="proceed",
    )
