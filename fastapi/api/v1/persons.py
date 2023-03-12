from http import HTTPStatus

from api.v1.api_models import Person, PersonDetail
from api.v1.utils import PaginatedParams
from services.person import PersonService, get_person_service

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/api/v1/persons")
index = {"model": "persons"}


@router.get(
    path="/{person_uuid}",
    response_model=PersonDetail,
    summary="Поиск персон по ID",
    description="Поиск персон по ID",
    response_description="Информация о персоналии",
)
async def person_details(
    person_uuid: str,
    person_service: PersonService = Depends(get_person_service),
) -> Person:
    params = {"uuid": person_uuid}
    person = await person_service.get_by_data(index, params)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Person not found",
        )
    return PersonDetail(**person[0])


@router.get(
    path="/search/",
    response_model=list[PersonDetail],
    summary="Персоналии",
    description="Полнотекстовый поиск по персоналиям",
    response_description="Список персоналий",
)
async def search_person(
    query: str,
    paginate: PaginatedParams = Depends(),
    person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    params = {"page": paginate.page, "size": paginate.size, "query": query}
    persons = await person_service.get_by_data(index, params)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Persons not found",
        )

    return [PersonDetail(**person) for person in persons]
