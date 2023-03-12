from models.model_mixin import ESBaseModel


class ESPerson(ESBaseModel):
    """Модель персоналий."""

    full_name: str


class ESPersonDetail(ESPerson):
    """Детальная модель персоналий."""

    role: str
    film_ids: list
