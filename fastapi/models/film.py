from models.genre import ESGenre
from models.model_mixin import ESBaseModel
from models.person import ESPerson


class ESFilm(ESBaseModel):
    """Модель фильмов."""

    title: str
    imdb_rating: float
    description: str
    genres: list[ESGenre] = []
    actors: list[ESPerson] = []
    writers: list[ESPerson] = []
    directors: list[ESPerson] = []
