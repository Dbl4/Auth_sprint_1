from uuid import UUID

from pydantic import BaseModel


class BaseUUID(BaseModel):
    uuid: UUID


class Person(BaseUUID):
    full_name: str


class PersonDetail(Person):
    role: str
    film_ids: list


class Genre(BaseUUID):
    name: str


class Film(BaseUUID):
    title: str
    imdb_rating: float
    description: str


class FilmDetail(Film):
    genres: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
