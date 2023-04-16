from fastapi import Query


class PaginatedParams:
    """
    Класс задает параметры для навигации документов.
    """

    def __init__(
        self,
        page: int = Query(
            1, alias="page[number]", ge=1, description="Номер страницы"
        ),
        size: int = Query(
            5,
            alias="page[size]",
            ge=1,
            le=10,
            description="Количество документов на странице",
        ),
    ) -> None:
        self.page = page
        self.size = size
