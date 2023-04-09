import uuid
from functools import lru_cache
from typing import Optional

from fastapi.param_functions import Depends

from db.base import AbstractStorage
from db.elastic import get_elastic
from models import films

from .base import AbstractService, GetById, GetList, Search


class FilmService(AbstractService, GetById, GetList, Search):

    async def get_by_id(self, film_id: uuid.UUID) -> Optional[films.Film]:
        try:
            doc = await self.storage.get('movies', film_id)
        except self.storage.not_found_error:
            return None

        if not doc:
            return None

        return films.Film(**doc['_source'])

    async def get_list(self, sort: str, size: int, page: int, filters: uuid.UUID) -> list[films.FilmInfo] | None:
        if filters:
            query = {"query": {
                    "bool": {
                        "should": [
                            {'nested': {
                                "path": "genre",
                                'query': {
                                    "bool": {
                                        "filter": [{"match_phrase": {"genre.id": filters}}]
                                    }
                                }
                            }},
                        ]
                    }
                }
                }
        else:
            query = None
        try:
            doc = await self.storage.search(
                index="movies",
                filter_path=['hits.hits._source.id', 'hits.hits._source.title', 'hits.hits._source.imdb_rating'],
                from_=page * size - size,
                size=size,
                sort=f"{sort[1:]}:desc" if sort[0] == '-' else f"{sort}:asc",
                body=query,
            )
        except RuntimeError:
            return None

        except self.storage.not_found_error:
            return None

        if not doc:
            return None

        return [films.FilmInfo(**film['_source']) for film in doc['hits']['hits']]

    async def search(self, query: str, page: int = 1, size: int = 50) -> list[films.FilmInfo] | None:
        doc = await self.storage.search(
            index="movies",
            body={"query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "title": query
                            }
                        },
                    ]
                }
            }
            },
            filter_path=['hits.hits._source.id', 'hits.hits._source.title', 'hits.hits._source.imdb_rating'],
            from_=page * size - size,
            size=size,
        )
        if not doc:
            return None

        return [films.FilmInfo(**film['_source']) for film in doc['hits']['hits']]


@lru_cache()
def get_film_service(
        storage: AbstractStorage = Depends(get_elastic),
) -> FilmService:
    return FilmService(storage)
