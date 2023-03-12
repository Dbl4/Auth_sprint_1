from typing import Optional

import aiohttp
import pytest
import pytest_asyncio

from tests.functional.settings import test_settings


@pytest_asyncio.fixture(scope='session')
async def aiohttp_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def aiohttp_get(aiohttp_client):
    async def inner(
        endpoint: str,
        query: Optional[dict] = None,
    ):
        url = f'{test_settings.service_url}{endpoint}'
        async with aiohttp_client.get(url, params=query) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        return (status, headers, body)

    return inner
