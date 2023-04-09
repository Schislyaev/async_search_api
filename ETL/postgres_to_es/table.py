"""
Yandex.Practicum sprint 3.

Pydantic tables section

Author: Petr Schislyaev
Date: 11/11/2023
"""


from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, validator


class ElasticIndex(BaseModel):
    id: str
    imdb_rating: float | None
    genre: Optional[list[Dict]]
    title: str
    description: Optional[str | None]
    director: list[Dict]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    actors: Optional[list[Dict]]
    writers: Optional[list[Dict]]
    modified: str

    @validator('director')
    @classmethod
    def validate_director(cls, value_to_validate):
        return value_to_validate if value_to_validate else []

    @classmethod
    def from_pg(cls, elem: dict):
        role_list = lambda role: [  # noqa: E731
            {'id': k.get('person_id'), 'name': k.get('person_name')}
            for k in elem['persons'] if k.get('person_role') == role]

        return cls(
            id=elem['id'],
            imdb_rating=elem['rating'],
            genre=[k for k in elem['genres']],
            title=elem['title'],
            description=elem['description'],
            actors_names=[actor['name'] for actor in role_list('actor')],
            writers_names=[writer['name'] for writer in role_list('writer')],
            actors=role_list('actor'),
            writers=role_list('writer'),
            director=role_list('director'),
            modified=str(elem['modified']),
        )

    def to_elastic(self):
        return {
            "_id": self.id,
            "_source": self.dict(exclude={'modified'}),
        }


class ElasticPerson(BaseModel):
    id: str
    full_name: str
    modified: datetime
    director_films: list[dict] | None
    actor_films: list[dict] | None
    writer_films: list[dict] | None

    @classmethod
    def from_pg(cls, elem: dict):
        return cls(**elem)

    def to_elastic(self):
        return {
            "_id": self.id,
            "_source": self.dict(exclude={'modified'}),
        }

    @validator('director_films')
    def validate_director_films(cls, value):
        return value if value else []

    @validator('actor_films')
    def validate_actor_films(cls, value):
        return value if value else []

    @validator('writer_films')
    def validate_writer_films(cls, value):
        return value if value else []


class ElasticGenre(BaseModel):
    id: str
    modified: datetime
    name: str

    @classmethod
    def from_pg(cls, elem: dict):
        return cls(**elem)

    def to_elastic(self):
        return {
            "_id": self.id,
            "_source": self.dict(exclude={'modified'}),
        }
