import json
from typing import List

import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings


@pytest_asyncio.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.elastic_url)
    yield client
    await client.close()


@pytest.fixture
def es_write_data(es_client):
    async def inner(es_data: List[dict], index):
        bulk_query = []
        for row in es_data:
            bulk_query.extend(
                [
                    json.dumps(
                        {"index": {"_index": index, "_id": row["uuid"]}}
                    ),
                    json.dumps(row),
                ]
            )
        str_query = "\n".join(bulk_query) + "\n"
        response = await es_client.bulk(body=str_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest.fixture
def es_delete_data(es_client):
    async def inner(es_data: List[dict], index):
        for row in es_data:
            await es_client.delete(index, row["uuid"])

    return inner
