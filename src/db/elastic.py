from elasticsearch import AsyncElasticsearch, NotFoundError

from core.config import config
from db.base import AbstractStorage


class ElasticStorage(AbstractStorage):
    elastic: AsyncElasticsearch = AsyncElasticsearch([config.elastic_connection_string])
    not_found_error = NotFoundError

    async def get(self, *args, **kwargs):
        return await self.elastic.get(*args, **kwargs)

    async def search(self, *args, **kwargs):
        return await self.elastic.search(*args, **kwargs)

    async def close(self):
        return await self.elastic.close()


es: ElasticStorage | None = None


async def get_elastic() -> ElasticStorage | None:
    return es
