from http import HTTPStatus

from api.v1.api_models import Genre
from api.v1.utils import PaginatedParams
from services.genre import GenreService, get_genre_service

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/api/v1/genres")
index = {"model": "genres"}


@router.get(
    path="/{genre_uuid}",
    response_model=Genre,
    summary="Поиск жанров по ID",
    description="Поиск жанров по ID",
    response_description="Информация о конкретном жанре",
)
async def genre_details(
    genre_uuid: str,
    genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    params = {"uuid": genre_uuid}
    genre = await genre_service.get_by_data(index, params)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Genre not found",
        )
    return Genre(**genre[0])


@router.get(
    path="/",
    response_model=list[Genre],
    summary="Список жанров",
    description="Список жанров",
    response_description="Список жанров",
)
async def list_genres(
    paginate: PaginatedParams = Depends(),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[Genre]:
    params = {"page": paginate.page, "size": paginate.size}
    es_genres = await genre_service.get_by_data(index, params)
    if not es_genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Genres not found",
        )

    return [Genre(**film) for film in es_genres]
