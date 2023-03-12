from http import HTTPStatus

from api.v1.api_models import Film, FilmDetail
from api.v1.utils import PaginatedParams
from services.film import FilmService, get_film_service

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter(prefix="/api/v1/films")
index = {"model": "movies"}


@router.get(
    path="/{film_uuid}",
    response_model=FilmDetail,
    summary="Поиск кинопроизведений по ID",
    description="Поиск кинопроизведений по ID",
    response_description="Полная информация о фильме",
)
async def film_details(
    film_uuid: str,
    film_service: FilmService = Depends(get_film_service),
) -> FilmDetail:
    params = {"uuid": film_uuid}
    film = await film_service.get_by_data(index, params)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="film not found",
        )
    return FilmDetail(**film[0])


@router.get(
    path="/search/",
    response_model=list[Film],
    summary="Поиск кинопроизведений",
    description="Полнотекстовый поиск по кинопроизведениям",
    response_description="Название и рейтинг фильма",
)
async def search_film(
    query: str,
    paginate: PaginatedParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    params = {"page": paginate.page, "size": paginate.size, "query": query}
    es_films = await film_service.get_by_data(index, params)
    if not es_films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="films not found",
        )

    return [Film(**film) for film in es_films]


@router.get(
    path="/",
    response_model=list[Film],
    summary="Главная страница кинопроизведений",
    description="Популярные фильмы",
    response_description="Название и рейтинг фильма",
)
async def list_films(
    sort: str = Query(
        "-imdb_rating",
        alias="sort",
        title="Сортировка по рейтингу",
        description="Сортирует по возрастанию и убыванию",
        regex="-?imdb_rating",
    ),
    paginate: PaginatedParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    params = {"page": paginate.page, "size": paginate.size, "sort": sort}
    es_films = await film_service.get_by_data(index, params)
    if not es_films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="films not found",
        )

    return [Film(**film) for film in es_films]


@router.get(
    path="/search/{person_uuid}/films",
    response_model=list[Film],
    description="Поиск фильмов по персоне",
    summary="Поиск фильмов по ID персоны",
    response_description="Поиск фильмов по ID персоны",
)
async def search_films_for_person(
    person_uuid: str,
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    params = {"model": {"person_uuid": person_uuid}}
    films = await film_service.get_by_data(index, params)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Films not found",
        )

    return [Film(**film) for film in films]


@router.get(
    path="/filter/{genre_uuid}/films",
    response_model=list[Film],
    description="Поиск фильмов по жанру",
    summary="Поиск фильмов по ID жанра",
    response_description="Поиск фильмов по ID жанра",
)
async def search_films_for_genre(
    genre_uuid: str,
    sort: str = Query(
        "-imdb_rating",
        alias="sort",
        title="Сортировка по рейтингу",
        description="Сортирует по возрастанию и убыванию",
        regex="-?imdb_rating",
    ),
    paginate: PaginatedParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    params = {
        "page": paginate.page,
        "size": paginate.size,
        "sort": sort,
        "model": {"genre_uuid": genre_uuid},
    }
    films_for_genre = await film_service.get_by_data(index, params)
    if not films_for_genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Films not found",
        )

    return [Film(**film) for film in films_for_genre]
