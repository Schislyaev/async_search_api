from pydantic import BaseModel

from models.base import DefaultModel
from models.genre import Genre


class FilmPerson(DefaultModel):
    name: str


class Film(DefaultModel):
    title: str
    imdb_rating: float | None
    description: str | None
    genre: list[Genre] | None
    actors: list[FilmPerson] | None
    writers: list[FilmPerson] | None
    director: list[FilmPerson] | None


class FilmInfo(DefaultModel):
    title: str
    imdb_rating: float


class FilmList(BaseModel):
    result: list[FilmInfo] | None
