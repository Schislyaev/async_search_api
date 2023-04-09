import uuid
from http import HTTPStatus

from cashews import cache
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from fastapi.routing import APIRouter

from core.config import config
from core.errors import Films
from services.film import FilmService, get_film_service

from .schemas.common_params import Pagination
from .schemas.film import Film, FilmList

err_msg = Films()

router = APIRouter()


@router.get(
    '/{film_id}',
    response_model=Film,
    name='Film_info',
    summary='Поиск фильма',
    description='Поиск фильма по id',
    response_description='Выводится вся информация о фильме,в том числе актеры, жанр, название и проч.',
)
@cache(
    ttl=config.REDIS_CACHE_TIMEOUT,
    key='{film_id}'
)
async def film_details(
        film_id: uuid.UUID = Query(..., title='id of requested film'),
        film_service: FilmService = Depends(get_film_service)
) -> Film:

    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err_msg.details_not_found)
    return film


@router.get(
    '/',
    response_model=FilmList,
    name='Films_list',
    summary='Список фильмов',
    description='Список фильмов в соответствие с параметрами страницы и сортировки',
    response_description='Выводится краткое описание фильмов',
)
@cache(
    ttl=config.REDIS_CACHE_TIMEOUT,
    key='sort_{sort}size{pagination.size}_page_{pagination.number}_filters_{filters}'
)
async def films_list(
        sort: str | None = Query(default='-imdb_rating'),
        filters: uuid.UUID | None = Query(description='genre uuid', default=None),
        film_service: FilmService = Depends(get_film_service),
        pagination: Pagination = Depends()
):

    films = await film_service.get_list(
        sort=sort,
        size=pagination.size,
        page=pagination.number,
        filters=filters
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err_msg.list_not_found)

    return {'result': films}


@router.get(
    '/search/',
    response_model=FilmList,
    name='Search_similar_films',
    summary='Полнотекстовый поиск',
    description='Поиск фильма по названию или его части, в соответствие с параметрами страницы и сортировки',
    response_description='Выводится краткое описание фильма',
)
@cache(
    ttl=config.REDIS_CACHE_TIMEOUT,
    key='size{pagination.size}_page_{pagination.number}_query_{query}_searching'
)
async def films_search(
        query: str = Query(default=None),
        film_service: FilmService = Depends(get_film_service),
        pagination: Pagination = Depends()
):
    films = await film_service.search(query=query, size=pagination.size, page=pagination.number)

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err_msg.search_not_found)

    return {'result': films}
