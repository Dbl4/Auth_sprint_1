"""Модель данных с валидацией."""
from typing import Optional

from pydantic import BaseModel


class BaseModelUUID(BaseModel):
    """Базовая модель с полем ID."""

    uuid: str


class PersonFW(BaseModelUUID):
    """Подмодель персоналии (директор, актер, сценарист)."""

    full_name: str


class GenreFW(BaseModelUUID):
    """Подмодель жанра для модели Filmwork."""

    name: str


class Filmwork(BaseModelUUID):
    """Модель кинопроизведения."""

    imdb_rating: float
    title: str
    description: Optional[str]
    actors_names: list[str] = []
    writers_names: list[str] = []
    directors_names: list[str] = []
    actors: list[PersonFW] = []
    writers: list[PersonFW] = []
    directors: list[PersonFW] = []
    genres: list[GenreFW] = []


class Genre(BaseModelUUID):
    """Модель жанра."""

    name: str
    description: str


class Person(BaseModelUUID):
    """Модель персоналии (директор, актер, сценарист)."""

    full_name: str
    role: str
    film_ids: list[str] = []
