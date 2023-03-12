from functools import lru_cache
from typing import Optional

from db.elastic import get_async_search
from db.redis import get_redis
from pydantic import ValidationError
from services.base import AsyncSearchEngine, BaseService, CacheStorage

from fastapi import Depends
from models.film import ESFilm


# FilmService содержит бизнес-логику по работе с фильмами.
# Никакой магии тут нет. Обычный класс с обычными методами.
# Этот класс ничего не знает про DI — максимально сильный и независимый.
class FilmService(BaseService):
    async def _get_list_models_by_params(
        self,
        index: dict,
        params: dict,
        order="desc",
    ) -> Optional[list[ESFilm]]:
        docs = await super()._get_list_models_by_params(index, params)
        try:
            return [
                ESFilm(**doc["_source"]).dict() for doc in docs["hits"]["hits"]
            ]
        except (TypeError, ValidationError):
            return None

    async def _get_by_uuid(
        self,
        index: dict,
        params: dict,
    ) -> Optional[ESFilm]:
        doc = await super()._get_by_uuid(index, params)
        try:
            return [ESFilm(**doc["_source"]).dict()]
        except (TypeError, ValidationError):
            return None

    async def _get_body(
        self,
        params: dict,
        order="desc",
    ) -> dict:
        body = await super()._get_body(params)
        params_query = params.get("query")
        params_model = params.get("model")
        sort = params.get("sort")
        if params_query:
            query = {
                "multi_match": {
                    "query": params_query,
                    "fields": ["title", "description"],
                },
            }
        elif params_model:
            query = await self.get_query_for_model(params_model)
        else:
            query = {"match_all": {}}

        if sort:
            order = "desc" if params["sort"].startswith("-") else "asc"

        return body | {
            "query": query,
            "sort": {"imdb_rating": {"order": order}},
        }

    async def get_query_for_model(self, params_model: dict) -> dict:
        """
        Получить тело запроса по uuid принимаемой модели.

          Args:
              params_model (dict): uuid для персон, жанров

          Returns:
              dict: Словарь, содержащий query для тела запроса
        """

        person_uuid = params_model.get("person_uuid")
        genre_uuid = params_model.get("genre_uuid")
        if person_uuid:
            return {
                "bool": {
                    "should": [
                        {
                            "nested": {
                                "path": "actors",
                                "query": {
                                    "term": {
                                        "actors.uuid": person_uuid,
                                    },
                                },
                            },
                        },
                        {
                            "nested": {
                                "path": "writers",
                                "query": {
                                    "term": {
                                        "writers.uuid": person_uuid,
                                    },
                                },
                            },
                        },
                        {
                            "nested": {
                                "path": "directors",
                                "query": {
                                    "term": {
                                        "directors.uuid": person_uuid,
                                    },
                                },
                            },
                        },
                    ],
                },
            }

        if genre_uuid:
            return {
                "nested": {
                    "path": "genres",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "term": {
                                        "genres.uuid": genre_uuid,
                                    },
                                },
                            ],
                        },
                    },
                },
            }

        return {}


# get_film_service — это провайдер FilmService.
# С помощью Depends он сообщает, что ему необходимы Redis и Elasticsearch
# Для их получения вы ранее создали функции-провайдеры в модуле db
# Используем lru_cache-декоратор, чтобы создать объект сервиса в едином
# экземпляре (синглтона) noqa: E501
@lru_cache()
def get_film_service(
    cache_db: CacheStorage = Depends(get_redis),
    db_asyc_search: AsyncSearchEngine = Depends(get_async_search),
) -> FilmService:
    return FilmService(cache_db, db_asyc_search)
