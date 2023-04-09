import uuid
from http import HTTPStatus

from cashews import cache
from fastapi import Query
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from core.config import config
from core.errors import Genres
from services.genre import GenreService, get_genre_service

from .schemas.genres import Genre

err_msg = Genres()
router = APIRouter()


@router.get(
    '/',
    response_model=list[Genre],
    summary='Список жанров',
    description='Список всех жанров, отсортированный по алфавиту',
    response_description='Список жанров',
)
@cache(
    ttl=config.REDIS_CACHE_TIMEOUT,
    key='genres'
)
async def genre_details(
        genre_service: GenreService = Depends(get_genre_service)
) -> list[Genre]:

    genres = await genre_service.search()

    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err_msg.details_not_found)

    return sorted([
        Genre(
            id=genre.id,
            name=genre.name
        ) for genre in genres
    ], key=lambda genre: genre.name)


@router.get(
    '/{genre_id}',
    response_model=Genre,
    summary='Детали жанра',
    description='Информация по жанру',
    response_description='ID и название жанра',
)
@cache(
    ttl=config.REDIS_CACHE_TIMEOUT,
    key='{genre_id}_genre_details'
)
async def genre_list(
        genre_id: uuid.UUID = Query(..., description='ID жанра в формате UUID'),
        genre_service: GenreService = Depends(get_genre_service)
) -> Genre:

    genre = await genre_service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err_msg.list_not_found)

    return Genre(id=genre.id, name=genre.name)
