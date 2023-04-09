from models.base import DefaultModel
from models.genre import Genre


class FilmPersonInfo(DefaultModel):
    name: str


class Film(DefaultModel):
    title: str
    imdb_rating: float | None
    description: str | None
    genre: list[Genre] | None
    actors: list[FilmPersonInfo] | None
    writers: list[FilmPersonInfo] | None
    director: list[FilmPersonInfo] | None


class FilmInfo(DefaultModel):
    title: str
    imdb_rating: float
