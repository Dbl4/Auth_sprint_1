import uuid
from http import HTTPStatus

import pytest
from faker import Faker


@pytest.mark.asyncio()
async def test_list_films(aiohttp_get, es_write_data, cleanup):
    await cleanup
    fake = Faker()
    es_data = [
        {
            "uuid": str(uuid.uuid4()),
            "title": "Title " + str(index),
            "imdb_rating": fake.random.randint(10, 100) / 10,
            "description": "Description " + str(index),
        }
        for index in range(10)
    ]
    await es_write_data(es_data, "movies")
    query_data = {"page": 1, "size": 5}

    status, headers, body = await aiohttp_get("/api/v1/films/", query_data)

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
async def test_retrieve_film(
    aiohttp_get,
    redis_client,
    es_delete_data,
    es_write_data,
    uuid,
    expected_code,
    cleanup,
):
    await cleanup
    fake = Faker()
    es_data = [
        {
            "uuid": "11111111-1111-1111-1111-111111111111",
            "title": "Existing Film",
            "imdb_rating": fake.random.randint(10, 100) / 10,
            "description": "Description for existing film",
        }
    ]
    await es_write_data(es_data, "movies")

    status, headers, body = await aiohttp_get(f"/api/v1/films/{uuid}")

    assert status == expected_code

    await es_delete_data(es_data, "movies")
    status, headers, body = await aiohttp_get(f"/api/v1/films/{uuid}")
    assert status == expected_code

    await redis_client.flushall()
    status, headers, body = await aiohttp_get(f"/api/v1/films/{uuid}")
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "uuid, title, imdb_rating, description, expected_code",
    [
        (
            "11111111-1111-1111-1111-111111111111",
            "Name",
            1.1,
            "",
            HTTPStatus.OK,
        ),
        (
            "22222222-2222-2222-2222-222222222222",
            "",
            1.2,
            "Description",
            HTTPStatus.OK,
        ),
        (
            "not-valid",
            "Name",
            1.0,
            "Description",
            HTTPStatus.NOT_FOUND,
        ),
        (
            "33333333-3333-3333-3333-333333333333",
            None,
            1.3,
            "Description",
            HTTPStatus.NOT_FOUND,
        ),
        (
            "44444444-4444-4444-4444-444444444444",
            "Name",
            1.4,
            None,
            HTTPStatus.NOT_FOUND,
        ),
        (
            "55555555-5555-5555-5555-555555555555",
            "Name",
            None,
            "Description",
            HTTPStatus.NOT_FOUND,
        ),
    ],
)
@pytest.mark.asyncio()
async def test_films_validation(
    aiohttp_get,
    es_write_data,
    uuid,
    title,
    imdb_rating,
    description,
    expected_code,
    cleanup,
):
    await cleanup
    es_data = [
        {
            "uuid": uuid,
            "title": title,
            "imdb_rating": imdb_rating,
            "description": description,
        }
    ]
    await es_write_data(es_data, "movies")

    status, headers, body = await aiohttp_get(f"/api/v1/films/{uuid}")

    assert status == expected_code


@pytest.mark.asyncio()
async def test_films_genre(aiohttp_get, es_write_data, cleanup):
    await cleanup
    fake = Faker()
    genre_uuid = "11111111-1111-1111-1111-111111111111"
    es_data = [
        {
            "uuid": str(uuid.uuid4()),
            "title": "Title",
            "imdb_rating": fake.random.randint(10, 100) / 10,
            "description": "Description",
            "genres": [{"uuid": genre_uuid, "name": "Genre Name"}],
        }
    ]
    await es_write_data(es_data, "movies")
    query_data = {"sort": "-imdb_rating", "page": 1, "size": 5}

    status, headers, body = await aiohttp_get(
        f"/api/v1/films/filter/{genre_uuid}/films", query_data
    )

    assert status == HTTPStatus.OK
    assert len(body) == 1


@pytest.mark.asyncio()
async def test_films_persons(aiohttp_get, es_write_data, cleanup):
    await cleanup
    fake = Faker()
    actor_uuid = "11111111-1111-1111-1111-111111111111"
    writer_uuid = "22222222-2222-2222-2222-222222222222"
    director_uuid = "33333333-3333-3333-3333-333333333333"
    es_data = [
        {
            "uuid": str(uuid.uuid4()),
            "title": "Title",
            "imdb_rating": fake.random.randint(10, 100) / 10,
            "description": "Description",
            "actors": [{"uuid": actor_uuid, "full_name": fake.name()}],
            "writers": [{"uuid": writer_uuid, "full_name": fake.name()}],
            "directors": [{"uuid": director_uuid, "full_name": fake.name()}],
        }
    ]
    await es_write_data(es_data, "movies")
    query_data = {"sort": "-imdb_rating", "page": 1, "size": 5}

    status, headers, body = await aiohttp_get(
        f"/api/v1/films/search/{actor_uuid}/films", query_data
    )

    assert status == HTTPStatus.OK
    assert len(body) == 1

    query_data = {"sort": "-imdb_rating", "page": 1, "size": 5}

    status, headers, body = await aiohttp_get(
        f"/api/v1/films/search/{writer_uuid}/films", query_data
    )

    assert status == HTTPStatus.OK
    assert len(body) == 1

    query_data = {"sort": "-imdb_rating", "page": 1, "size": 5}

    status, headers, body = await aiohttp_get(
        f"/api/v1/films/search/{director_uuid}/films", query_data
    )

    assert status == HTTPStatus.OK
    assert len(body) == 1
