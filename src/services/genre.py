from functools import lru_cache

from fastapi.param_functions import Depends

from db.base import AbstractStorage
from db.elastic import get_elastic
from models.genre import Genre

from .base import AbstractService, GetById, Search


class GenreService(AbstractService, GetById, Search):

    async def get_by_id(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.storage.get('genres', genre_id)
        except self.storage.not_found_error:
            return None

        if not doc:
            return None

        return Genre(**doc['_source'])

    async def search(self) -> list[Genre] | None:
        try:
            doc = await self.storage.search(index='genres', body={"query": {"match_all": {}}})
        except self.storage.not_found_error:
            return None

        if not doc:
            return None

        return [Genre(**genre['_source']) for genre in doc['hits']['hits']]


@lru_cache()
def get_genre_service(
        storage: AbstractStorage = Depends(get_elastic)
) -> GenreService:
    return GenreService(storage)
