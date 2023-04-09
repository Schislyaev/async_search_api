import uuid
from http import HTTPStatus

from cashews import cache
from fastapi import Query
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from core.config import config
from core.errors import Persons
from services.person import PersonService, get_person_service

from .schemas.common_params import Pagination
from .schemas.persons import Film, Person, PersonData

err_msg = Persons()
router = APIRouter()


@router.get(
    '/search',
    response_model=list[PersonData],
    summary='Полнотекстовый поиск',
    description='Поиск по именам и/или названиям фильмов. Можно использовать wildcards.',
    response_description='Выводятся карточки персонажей, найденные по имени или по фильмам в которых они участвовали',
)
@cache(
    ttl=config.REDIS_CACHE_TIMEOUT,
    key="{query}_size_{pagination.size}_page_{pagination.number}_search"
)
async def persons_search(
        query: str = Query('George*', description='Запрос', max_length=50),
        person_service: PersonService = Depends(get_person_service),
        pagination: Pagination = Depends()
) -> list[PersonData]:

    results = await person_service.search(query, page=pagination.number, size=pagination.size)

    if not results:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err_msg.search_not_found)

    roles_temp = lambda elem: [  # noqa: E731
        'director' if elem.director_films else None,
        'actor' if elem.actor_films else None,
        'writer' if elem.writer_films else None
    ]

    return [
                PersonData(
                    id=result.id,
                    full_name=result.full_name,
                    roles=[role for role in roles_temp(result) if role],
                    film_ids=list(
                        set(
                            [film.id for film in result.actor_films] +
                            [film.id for film in result.writer_films] +
                            [film.id for film in result.director_films]
                        )
                    )
                ) for result in results
            ]


@router.get(
    '/{person_id}',
    response_model=PersonData,
    summary='Поиск по ID',
    description='Поиск по ID персоны',
    response_description='Выводятся карточки персонажи с перечислением всех его ролей и ID фильмов',
)
@cache(
    ttl=config.REDIS_CACHE_TIMEOUT,
    key='{person_id}_person_details'
)
async def person_details(
        person_id: uuid.UUID = Query(..., description='ID персонажа'),
        person_service: PersonService = Depends(get_person_service)
) -> PersonData:
    """В соответствии с ТЗ"""

    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err_msg.details_not_found)

    roles_temp = [
        'director' if person.director_films else None,
        'actor' if person.actor_films else None,
        'writer' if person.writer_films else None
    ]

    return PersonData(
        id=person.id,
        full_name=person.full_name,
        roles=[role for role in roles_temp if role],
        film_ids=list(
            set(
                [film.id for film in person.actor_films] +
                [film.id for film in person.writer_films] +
                [film.id for film in person.director_films]
            )
        )
    )


@router.get(
    '/{person_id}/detailed',
    response_model=Person,
    summary='Поиск по ID (с деталями фильмов)',
    description='Поиск по ID персоны',
    response_description='Выводятся карточки персонажи с детальным перечислением всех его ролей и фильмов',
)
@cache(
    ttl=config.REDIS_CACHE_TIMEOUT,
    key='{person_id}_person_details_detailed'
)
async def person_details_detailed(
        person_id: uuid.UUID = Query(..., description='ID персонажа'),
        person_service: PersonService = Depends(get_person_service)
) -> Person:
    """Копия ES индекса"""

    person = await person_service.get_by_id(person_id)

    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err_msg.details_detailed_not_found)

    return Person(
        id=person.id,
        full_name=person.full_name,
        director_films=person.director_films,
        actor_films=person.actor_films,
        writer_films=person.writer_films
    )


@router.get(
    '/{person_id}/film',
    response_model=list[Film],
    summary='Поиск фильмов по ID',
    description='Поиск фильмов в которых принимал участие персонаж',
    response_description='Выводится список карточек фильмов персонажа, отсортированных по рейтингу',
)
@cache(
    ttl=config.REDIS_CACHE_TIMEOUT,
    key='{person_id}_{sorting}_person_films_details'
)
async def person_films_details(
        person_id: uuid.UUID = Query(..., description='ID персонажа'),
        sorting: bool = Query(True, description='Сортировка по убыванию рейтинга'),
        person_service: PersonService = Depends(get_person_service)
) -> list[Film]:

    person = await person_service.get_by_id(person_id)

    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err_msg.films_details_not_found)

    # Для сортировки и хеширования (для возможности оставить уникальные объекты в списке)
    # были добавлены дополнительные методы в класс person.PersonFilm
    films = sorted(
        list(
            set(
                person.actor_films +
                person.writer_films +
                person.director_films
            )
        ), reverse=sorting
    )

    return [
        Film(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        ) for film in films
    ]
