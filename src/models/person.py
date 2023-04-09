from models.base import DefaultModel


class PersonFilm(DefaultModel):
    title: str
    imdb_rating: float

    def __hash__(self):
        return int(str(self.id).replace('-', ''), 16)

    def __lt__(self, other):
        return self.imdb_rating < other.imdb_rating


class Person(DefaultModel):
    full_name: str
    director_films: list[PersonFilm]
    actor_films: list[PersonFilm]
    writer_films: list[PersonFilm]
