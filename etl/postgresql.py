"""Модуль извлечения данных из PostgreSQL."""

import logging
from datetime import datetime
from typing import Optional

from psycopg2.extensions import connection as _connection

from models import BaseModelUUID


class Extractor:
    """Класс для извлечения данных из PostgreSQL."""

    def __init__(
        self,
        sql: str,
        connection: _connection,
        timepoint: Optional[datetime],
        model: BaseModelUUID,
        schema: str = "content",
        batch_size: int = 50,
    ) -> None:
        """Инициализатор класса.

        Args:
            sql: SQL запрос для получения данных.
            connection: Установленное подключение к PostgreSQL.
            timepoint: Дата, начиная с которой искать изменения.
            model: Модель данных.
            schema: Схема базы данных, в которой расположены таблицы.
            batch_size: Количество записей в одном пакете.
        """
        self.logger = logging.getLogger("etl")
        self.connection = connection
        self.timepoint = timepoint
        self.model = model
        self.sql = sql.format(schema=schema)
        self.batch_size = batch_size

    def __iter__(self):
        """Возвращает объект итератора.

        Returns:
            object: Объект итератора.
        """
        self.cursor = self.connection.cursor()
        self.cursor.arraysize = self.batch_size
        self.cursor.execute(self.sql, {"timepoint": self.timepoint})
        self.logger.info("Extracted " + str(self.cursor.rowcount) + " rows")
        return self

    def __next__(self):
        """Возвращает пакет данных.

        Raises:
            StopIteration: Окончание итераций.

        Returns:
            list: Пакет записей.
        """
        rows = self.cursor.fetchmany()
        if not rows:
            raise StopIteration

        result = []
        for item in rows:
            result.append(self.model(**dict(item)))
        return result
