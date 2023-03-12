from models.model_mixin import ESBaseModel


class ESGenre(ESBaseModel):
    """Модель жанров."""

    name: str
