from functools import lru_cache
from typing import Optional

from db.elastic import get_async_search
from db.redis import get_redis
from pydantic import ValidationError
from services.base import AsyncSearchEngine, BaseService, CacheStorage

from fastapi import Depends
from models.genre import ESGenre


class GenreService(BaseService):
    async def _get_list_models_by_params(
        self,
        index: dict,
        params: dict,
        *args,
    ) -> Optional[list[ESGenre]]:
        docs = await super()._get_list_models_by_params(index, params)
        try:
            return [
                ESGenre(**doc["_source"]).dict()
                for doc in docs["hits"]["hits"]
            ]
        except (TypeError, ValidationError):
            return None

    async def _get_by_uuid(
        self,
        index: dict,
        params: dict,
    ) -> Optional[list[ESGenre]]:
        doc = await super()._get_by_uuid(index, params)
        try:
            return [ESGenre(**doc["_source"]).dict()]
        except (TypeError, ValidationError):
            return None


# get_genre_service — это провайдер GenreService.
# С помощью Depends он сообщает, что ему необходимы Redis и Elasticsearch
# Для их получения вы ранее создали функции-провайдеры в модуле db
# Используем lru_cache-декоратор, чтобы создать объект сервиса в едином
# экземпляре (синглтона) noqa
@lru_cache()
def get_genre_service(
    cache_db: CacheStorage = Depends(get_redis),
    db_asyc_search: AsyncSearchEngine = Depends(get_async_search),
) -> GenreService:
    return GenreService(cache_db, db_asyc_search)
