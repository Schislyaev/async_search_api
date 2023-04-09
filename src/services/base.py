import uuid
from abc import ABC, abstractmethod

from db.base import AbstractStorage
from models.base import DefaultModel


class AbstractService(ABC):
    def __init__(self, storage: AbstractStorage):
        self.storage = storage


class GetById(ABC):
    @abstractmethod
    async def get_by_id(
            self,
            item_id: uuid.UUID
    ) -> DefaultModel | None:
        ...


class Search(ABC):
    @abstractmethod
    async def search(
            self,
            **kwargs
    ) -> DefaultModel | None:
        ...


class GetList(ABC):
    @abstractmethod
    async def get_list(
            self, sort: str,
            size: int,
            page: int,
            filters: str
    ) -> DefaultModel | None:
        ...
