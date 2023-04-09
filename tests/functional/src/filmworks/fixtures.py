import pytest
from elasticsearch import AsyncElasticsearch, helpers
from functional.testdata.filmworks_data import FILMWORK_INDEX, FILMWORKS_DATA


@pytest.fixture(scope='session', autouse=True)
async def load_filmworks(es_client: AsyncElasticsearch):
    await es_client.indices.create(
        index='movies',
        body=FILMWORK_INDEX,
        ignore=400
    )

    await helpers.async_bulk(es_client, FILMWORKS_DATA, index='movies')

    await es_client.indices.refresh(index='movies')
