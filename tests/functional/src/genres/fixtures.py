import pytest
from elasticsearch import AsyncElasticsearch, helpers
from functional.testdata.genres_data import GENRES_DATA, GENRES_INDEX


@pytest.fixture(scope='session', autouse=True)
async def load_genres(es_client: AsyncElasticsearch):
    await es_client.indices.create(
        index='genres',
        body=GENRES_INDEX,
        ignore=400
    )

    await helpers.async_bulk(es_client, GENRES_DATA, index='genres')

    await es_client.indices.refresh(index='genres')
