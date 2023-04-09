import pytest
from elasticsearch import AsyncElasticsearch, helpers
from functional.testdata.persons_data import PERSONS_DATA, PERSONS_INDEX


@pytest.fixture(scope='session', autouse=True)
async def load_persons(es_client: AsyncElasticsearch):
    await es_client.indices.create(
        index='persons',
        body=PERSONS_INDEX,
        ignore=400
    )

    await helpers.async_bulk(es_client, PERSONS_DATA, index='persons')

    await es_client.indices.refresh(index='persons')
