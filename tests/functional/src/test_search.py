import uuid
from http import HTTPStatus

import pytest
from faker import Faker

from tests.functional.src.test_persons import Role

SIZE = 5


def get_es_data(index: str) -> list[dict]:
    fake = Faker()

    if index == "movies":
        return [
            {
                "uuid": str(fake.uuid4()),
                "imdb_rating": fake.random.randint(10, 100) / 10,
                "title": "The Star",
                "description": str(fake.text()),
                "actors": [
                    {
                        "uuid": str(fake.uuid4()),
                        "full_name": "Actor",
                    }
                ],
                "writers": [
                    {
                        "uuid": str(fake.uuid4()),
                        "full_name": "Writer",
                    }
                ],
                "directors": [
                    {
                        "uuid": str(fake.uuid4()),
                        "full_name": "Director",
                    }
                ],
                "genres": [
                    {
                        "uuid": str(fake.uuid4()),
                        "name": fake.word(),
                    }
                ],
            }
            for _ in range(SIZE * 2)
        ]

    if index == "persons":
        return [
            {
                "uuid": str(uuid.uuid4()),
                "full_name": "Han Solo",
                "role": str(fake.enum(Role).value),
                "film_ids": [str(uuid.uuid4())],
            }
            for _ in range(SIZE * 2)
        ]

    return []


@pytest.mark.parametrize(
    "search, index, api_name, expected_code, length",
    [
        ("The Star", "movies", "films", HTTPStatus.OK, SIZE),
        ("Кин_дза-дза", "movies", "films", HTTPStatus.NOT_FOUND, 1),
        ("Han Solo", "persons", "persons", HTTPStatus.OK, SIZE),
        ("Господин ПЖ", "persons", "persons", HTTPStatus.NOT_FOUND, 1),
    ],
)
@pytest.mark.asyncio()
async def test_search(
    aiohttp_get,
    cleanup,
    search,
    index,
    api_name,
    expected_code,
    length,
    es_write_data,
    es_delete_data,
):
    await cleanup
    # проверим, что фильма или персоны не существует, если в базе нет данных
    query_data = {"query": search, "page": 1, "size": SIZE}

    status, headers, body = await aiohttp_get(
        f"/api/v1/{api_name}/search/", query_data
    )

    assert status == HTTPStatus.NOT_FOUND

    # заполним базу данными
    es_data = get_es_data(index)
    await es_write_data(es_data, index)

    # проверим работу эластика
    status, headers, body = await aiohttp_get(
        f"/api/v1/{api_name}/search/", query_data
    )

    assert status == expected_code
    assert len(body) == length

    # проверим работу редиса, удалив данные из эластика
    await es_delete_data(es_data, index)

    status, headers, body = await aiohttp_get(
        f"/api/v1/{api_name}/search/", query_data
    )

    assert status == expected_code
    assert len(body) == length
