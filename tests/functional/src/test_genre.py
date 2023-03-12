import uuid
from http import HTTPStatus

import pytest


@pytest.mark.asyncio()
async def test_list_genres(
    aiohttp_get, es_write_data, es_delete_data, cleanup
):
    await cleanup
    es_data = [
        {
            "uuid": str(uuid.uuid4()),
            "name": "Genre " + str(index),
            "description": "Description " + str(index),
        }
        for index in range(10)
    ]
    await es_write_data(es_data, "genres")
    query_data = {"page": 1, "size": 5}
    status, headers, body = await aiohttp_get(f"/api/v1/genres/", query_data)

    assert status == HTTPStatus.OK
    assert len(body) == 5


@pytest.mark.parametrize(
    "uuid, expected_code",
    [
        ("11111111-1111-1111-1111-111111111111", HTTPStatus.OK),
        ("00000000-0000-0000-0000-000000000000", HTTPStatus.NOT_FOUND),
        ("not-valid", HTTPStatus.NOT_FOUND),
    ],
)
@pytest.mark.asyncio()
async def test_retrieve_genres(
    aiohttp_get,
    redis_client,
    es_delete_data,
    es_write_data,
    uuid,
    expected_code,
    cleanup,
):
    await cleanup
    es_data = [
        {
            "uuid": "11111111-1111-1111-1111-111111111111",
            "name": "Existing Genre",
            "description": "Description for existing genre",
        }
    ]
    await es_write_data(es_data, "genres")

    status, headers, body = await aiohttp_get(f"/api/v1/genres/{uuid}")

    assert status == expected_code

    await es_delete_data(es_data, "genres")
    status, headers, body = await aiohttp_get(f"/api/v1/genres/{uuid}")
    assert status == expected_code

    await redis_client.flushall()
    status, headers, body = await aiohttp_get(f"/api/v1/genres/{uuid}")
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "uuid, name, description, expected_code",
    [
        ("11111111-1111-1111-1111-111111111111", "Name", "", HTTPStatus.OK),
        (
            "22222222-2222-2222-2222-222222222222",
            "",
            "Description",
            HTTPStatus.OK,
        ),
        ("not-valid", "Name", "Description", HTTPStatus.NOT_FOUND),
        (
            "33333333-3333-3333-3333-333333333333",
            None,
            "Description",
            HTTPStatus.NOT_FOUND,
        ),
        ("44444444-4444-4444-4444-444444444444", "Name", None, HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio()
async def test_genres_validation(
    aiohttp_get,
    es_delete_data,
    es_write_data,
    uuid,
    name,
    description,
    expected_code,
    cleanup,
):
    await cleanup
    es_data = [
        {
            "uuid": uuid,
            "name": name,
            "description": description,
        }
    ]
    await es_write_data(es_data, "genres")

    status, headers, body = await aiohttp_get(f"/api/v1/genres/{uuid}")

    assert status == expected_code
