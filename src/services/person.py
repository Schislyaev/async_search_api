import uuid
from functools import lru_cache

from fastapi.param_functions import Depends

from db.base import AbstractStorage
from db.elastic import get_elastic
from models.person import Person

from .base import AbstractService, GetById, Search


class PersonService(AbstractService, GetById, Search):

    async def get_by_id(self, person_id: uuid.UUID) -> Person | None:

        try:
            doc = await self.storage.get('persons', person_id)
        except self.storage.not_found_error:
            return None

        if not doc:
            return None

        return Person(**doc['_source'])

    async def search(self, query: str, page: int, size: int) -> list[Person] | None:
        try:
            doc = await self.storage.search(
                index="persons",
                body={
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "query_string":
                                        {
                                            "query": query
                                        }
                                },
                                {'nested': {
                                    "path": "actor_films",
                                    'query': {
                                        "bool": {
                                            "filter": [{"match_phrase": {"actor_films.title": query}}]
                                        }
                                    }
                                }},
                                {"nested": {
                                    "path": "writer_films",
                                    "query": {
                                        "bool": {
                                            "filter": [{"match_phrase": {"writer_films.title": query}}]
                                        }
                                    }
                                }},
                                {"nested": {
                                    "path": "director_films",
                                    "query": {
                                        "bool": {
                                            "filter": [{"match_phrase": {"director_films.title": query}}]
                                        }
                                    }
                                }}
                            ]
                        }
                    }
                },
                _source=True,
                from_=page * size - size,
                size=size,
            )
        except self.storage.not_found_error:
            return None
        if not doc:
            return None
        return [Person(**person['_source']) for person in doc['hits']['hits']]


@lru_cache()
def get_person_service(
        storage: AbstractStorage = Depends(get_elastic)
) -> PersonService:
    return PersonService(storage)
