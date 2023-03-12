"""Класс State реализует хранение состояния."""
import abc
import json
from typing import Any


class BaseStorage:
    """Базовый класс хранилища."""

    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище.

        Args:
            state: Состояние для записи в хранище.
        """

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища."""


class JsonFileStorage(BaseStorage):
    """Класс хранилища в файле формата JSON."""

    def __init__(self, file_path=None):
        """Инициализатор класса.

        Args:
            file_path: Путь к файлу хранилища.
        """
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        """Записывает состояние в хранилище.

        Args:
            state: Состояние для записи в хранилице.
        """
        with open(self.file_path, "w") as json_file:
            json.dump(state, json_file)

    def retrieve_state(self) -> dict:
        """Читает состояние из хранилица.

        Returns:
            dict: Состояние, извлеченное из хранилица.
        """
        try:
            with open(self.file_path, "r") as json_file:
                state = json.load(json_file)
        except FileNotFoundError:
            state = {}
        if not state:
            state = {}
        return state


class State:
    """Класс для хранения состояния при работе с данными."""

    def __init__(self, storage: BaseStorage):
        """Инициализатор класса.

        Args:
            storage: Используемое хранилице.
        """
        self.storage = storage
        self.state = storage.retrieve_state()

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа.

        Args:
            key: Ключ
            value: Значение ключа
        """
        self.state[key] = value
        self.storage.save_state(self.state)

    def get_state(self, key: str, default=None) -> Any:
        """Получить состояние по определённому ключу.

        Args:
            key: Ключ
            default: Возвращаемое значение, если не найдено в хранилище

        Returns:
            Any: Значение ключа.
        """
        return self.state.get(key, default)
