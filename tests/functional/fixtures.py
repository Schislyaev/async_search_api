import asyncio
# import warnings

import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from functional.settings import test_settings


@pytest.fixture(scope='session')
def event_loop():
    # with warnings.catch_warnings():
    #     warnings.filterwarnings("ignore", category=DeprecationWarning)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def es_client(event_loop):
    client = AsyncElasticsearch(
        hosts=f'http://{test_settings.es_host}:{test_settings.es_port}',
        validate_cert=False,
        use_ssl=False
    )

    yield client

    await client.close()


@pytest.fixture(scope='session')
async def redis_client(event_loop):
    redis = await aioredis.from_url(f'redis://{test_settings.redis_host}:{test_settings.redis_port}')

    yield redis

    await redis.close()


@pytest.fixture(autouse=True)
async def set_up_and_flush_cache(redis_client):
    await redis_client.flushdb()
