import uuid

from models.base import DefaultModel


class PersonFilm(DefaultModel):
    title: str
    imdb_rating: float


class Person(DefaultModel):
    full_name: str
    director_films: list[PersonFilm] | None
    actor_films: list[PersonFilm] | None
    writer_films: list[PersonFilm] | None


class Film(DefaultModel):
    title: str
    imdb_rating: float


class PersonData(DefaultModel):
    full_name: str
    roles: list[str]
    film_ids: list[uuid.UUID]
