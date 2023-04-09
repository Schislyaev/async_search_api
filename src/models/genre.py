import uuid

from models.base import DefaultModel


class Genre(DefaultModel):
    id: uuid.UUID
    name: str

    def __lt__(self, other):
        return self.name < other.name
