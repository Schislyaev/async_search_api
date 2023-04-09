from abc import ABC, abstractmethod
from typing import Any


class AbstractStorage(ABC):
    not_found_error: Any = None

    @abstractmethod
    async def get(self, *args, **kwargs):
        ...

    @abstractmethod
    async def search(self, *args, **kwargs):
        ...

    @abstractmethod
    async def close(self):
        ...
