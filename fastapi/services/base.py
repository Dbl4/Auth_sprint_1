from abc import ABC, abstractmethod
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel
from redis import asyncio as aioredis

BASE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class CacheModel(BaseModel):
    """Модель для проброски данных в редис."""

    name: str
    value: list


class BaseStorage(ABC):
    """Абстрактный класс хранилища данных."""

    def __init__(self, db_cache, db_search):
        self.db_cache = db_cache
        self.db_search = db_search


class AsyncSearchEngine(BaseStorage):
    """Абстрактный класс для поискового движка."""

    @abstractmethod
    async def _get_by_uuid(self, index: dict, params: dict) -> Optional[list]:
        pass

    @abstractmethod
    async def _get_list_models_by_params(
        self,
        index: dict,
        params: dict,
        *args,
    ) -> Optional[list]:
        pass


class CacheStorage(BaseStorage):
    """Абстрактный класс БД для кэширования."""

    @abstractmethod
    async def _get_key_cache(self, index: dict, params: dict) -> str:
        pass

    @abstractmethod
    async def _put_to_cache(self, cache_model: CacheModel) -> None:
        pass

    @abstractmethod
    async def _get_from_cache(self, key: str) -> Optional[list]:
        pass


class ElasticSearchEngine(AsyncSearchEngine):
    """Класс, использующий в качестве поискового движка ElasticSearch."""

    async def _get_by_uuid(self, index: dict, params: dict) -> Optional[list]:
        """
        Базовый метод. Получить doc индекса по uuid.

          Args:
              index (dict): Индекс ElasticSearch
              params(dict): Параметры от пользователя

          Returns:
              Optional[list]: Список документов из ElasticSearch
        """

        try:
            return await self.db_search.get(index["model"], params["uuid"])
        except NotFoundError:
            return None

    async def _get_list_models_by_params(
        self,
        index: dict,
        params: dict,
        *args,
    ) -> Optional[list]:
        """
        Базовый метод. Получить docs индекса по телу запроса.

          Args:
              index (dict): Индекс ElasticSearch
              params (dict): Параметры от пользователя
              *args: Дополнительные аргументы (опционально)

          Returns:
              Optional[list]: Список документов из ElasticSearch
        """

        body = await self._get_body(params, *args)
        try:
            return await self.db_search.search(index=index["model"], body=body)
        except NotFoundError:
            return None

    async def _get_body(self, params: dict, *args) -> dict:
        """
        Базовый метод. Получить тело запроса.

          Args:
              params (dict): Параметры от пользователя
              *args: Дополнительные аргументы (опционально)

          Returns:
              dict: Словарь (тело запроса в ElasticSearch)
        """

        size = params.get("size")
        page = params.get("page")
        if size and page:
            return {"size": size, "from": (page - 1) * size}
        return {}


class RedisStorage(CacheStorage):
    """Класс, использующий Redis для кэширования данных."""

    async def _get_key_cache(self, index: dict, params: dict) -> str:
        return f"{str(index)}::{str(params)}"

    async def _get_from_cache(self, key: str) -> Optional[list]:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.db_cache.get(key)
        if not data:
            return None

        return CacheModel.parse_raw(data).value

    async def _put_to_cache(self, cache_model: CacheModel) -> None:
        await self.db_cache.set(
            cache_model.name,
            cache_model.json(),
            ex=BASE_CACHE_EXPIRE_IN_SECONDS,
        )


class BaseService(ElasticSearchEngine, RedisStorage):
    """Базовый класс сервиса."""

    def __init__(
        self,
        redis: Optional[aioredis.Redis],
        elastic: Optional[AsyncElasticsearch],
    ):
        super().__init__(redis, elastic)

    async def get_by_data(self, index: dict, params: dict) -> Optional[list]:
        """
        Основной метод получения данных из Elasticsearch или Redis.

          Args:
              index (dict): Индекс ElasticSearch
              params(dict): Параметры от пользователя

          Returns:
              Optional[list]: Список документов из ElasticSearch
        """

        # составим ключ, по которому будет вестись поиск в redis
        key = await self._get_key_cache(index, params)
        data = await self._get_from_cache(key)
        if not data:
            # если в параметрах есть uuid, считаем что
            # это запрос на получения определенного
            # фильма или жанра или персоны.
            # Либо это запрос на получение их списка.
            if params.get("uuid"):
                data = await self._get_by_uuid(index, params)
            else:
                data = await self._get_list_models_by_params(index, params)
            if not data:
                return None
            await self._put_to_cache(CacheModel(name=key, value=data))

        return data
