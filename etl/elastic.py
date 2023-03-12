"""Модуль загрузки данных в Elasticsearch."""

from contextlib import contextmanager

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from models import BaseModelUUID


@contextmanager
def connect(host):
    """Менеджер контекста для безопасного подключения к Elasticsearch.

    Args:
        host: URL подключения к Elasticsearch.

    Yields:
        Подключение к Elasticsearch.
    """
    es = Elasticsearch(host)
    yield es
    es.close()


class Loader:
    """Класс загрузки данных в Elasticsearch."""

    index: str

    def __init__(self, connection, index: str):
        """Инициализатор класса.

        Args:
            connection: Подключение к Elasticsearch.
            index: Используемый для записи индекс БД.
        """
        self.connection = connection
        self.index = index

    def load_batch(self, batch: list[BaseModelUUID]):
        """Загружает пакет фильмов.

        Args:
            batch: Пакет фильмов.
        """
        documents = [
            {"_index": self.index, "_id": row.uuid, "_source": row.dict()}
            for row in batch
        ]
        bulk(self.connection, documents)
