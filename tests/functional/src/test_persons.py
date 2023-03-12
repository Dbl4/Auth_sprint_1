from enum import Enum
from http import HTTPStatus

import pytest
from faker import Faker


class Role(Enum):
    ACTOR = "actor"
    WRITER = "writer"
    DIRECTOR = "director"


def generate_es_document(
    index=None,
    uuid=None,
    full_name=None,
    role=None,
    film_ids=None,
):
    fake = Faker(["es_ES", "en_US", "ja_JP", "ru_RU"])
    index = index if index else ""
    uuid = uuid if uuid else fake.uuid4()
    full_name = (
        full_name if full_name else fake.name() + " full name" + str(index)
    )
    role = role if role else str(fake.enum(Role).value)
    film_ids = film_ids if film_ids else [str(fake.uuid4()), str(fake.uuid4())]
    return {
        "uuid": str(uuid),
        "full_name": full_name,
        "role": role,
        "film_ids": film_ids,
    }


@pytest.mark.asyncio()
async def test_search_persons(aiohttp_get, es_write_data, cleanup):
    await cleanup
    es_data = [generate_es_document(index) for index in range(10)]
    await es_write_data(es_data, "persons")
    query_data = {"query": "full", "page": 1, "size": 5}

    status, headers, body = await aiohttp_get(
        f"/api/v1/persons/search/", query_data
    )

    assert status == HTTPStatus.OK
    assert len(body) == 5

    query_data = {"query": "name2", "page": 1, "size": 5}

    status, headers, body = await aiohttp_get(
        f"/api/v1/persons/search/", query_data
    )

    assert status == HTTPStatus.OK
    assert len(body) == 1


@pytest.mark.parametrize(
    "uuid, expected_code",
    [
        ("11111111-1111-1111-1111-111111111111", HTTPStatus.OK),
        ("00000000-0000-0000-0000-000000000000", HTTPStatus.NOT_FOUND),
        ("not-valid", HTTPStatus.NOT_FOUND),
    ],
)
@pytest.mark.asyncio()
async def test_retrieve_person(
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
    # Делаем один существующий документ и проверяем, что найдет существующий
    # и не найдет несуществующий
    es_data = [
        generate_es_document(uuid="11111111-1111-1111-1111-111111111111")
    ]
    await es_write_data(es_data, "persons")

    status, headers, body = await aiohttp_get(f"/api/v1/persons/{uuid}")

    assert status == expected_code

    await es_delete_data(es_data, "persons")
    status, headers, body = await aiohttp_get(f"/api/v1/persons/{uuid}")
    assert status == expected_code

    await redis_client.flushall()
    status, headers, body = await aiohttp_get(f"/api/v1/persons/{uuid}")
    assert status == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "uuid, full_name, role, film_ids, expected_code",
    [
        (
            "11111111-1111-1111-1111-111111111111",
            "Name",
            "actor",
            [],
            HTTPStatus.OK,
        ),
        (
            "22222222-2222-2222-2222-222222222222",
            "",
            "writer",
            [],
            HTTPStatus.OK,
        ),
        ("not-valid", "Name", "actor", [], HTTPStatus.NOT_FOUND),
        (
            "33333333-3333-3333-3333-333333333333",
            None,
            "actor",
            [],
            HTTPStatus.NOT_FOUND,
        ),
        (
            "44444444-4444-4444-4444-444444444444",
            "Name",
            None,
            [],
            HTTPStatus.NOT_FOUND,
        ),
    ],
)
@pytest.mark.asyncio()
async def test_persons_validation(
    aiohttp_get,
    es_delete_data,
    es_write_data,
    uuid,
    full_name,
    role,
    film_ids,
    expected_code,
    cleanup,
):
    await cleanup
    # Здесь generate_es_document неприменим,
    # потому что нам надо присвоить значение None
    es_data = [
        {
            "uuid": uuid,
            "full_name": full_name,
            "role": role,
            "film_ids": film_ids,
        }
    ]
    await es_write_data(es_data, "persons")

    status, headers, body = await aiohttp_get(f"/api/v1/persons/{uuid}")

    assert status == expected_code
