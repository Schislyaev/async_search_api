import aioredis
import uvicorn
from cashews import cache
from fastapi.applications import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from api.v1 import films, genres, persons
from core.config import config
from core.logger import LOGGING
from db import elastic, redis

app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESCRIPTION,
    version=config.PROJECT_VERSION,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    openapi_tags=[
        {
            'name': 'Films',
            'description': 'Поиск по фильмам'
        },
        {
            'name': 'Persons',
            'description': 'Поиск по персоналиям'
        },
        {
            'name': 'Genres',
            'description': 'Поиск по жанрам'
        },
    ]

)

app.include_router(films.router, prefix='/api/v1/films', tags=['Films'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['Persons'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['Genres'])


@app.middleware("http")
async def add_from_cache_headers(request: Request, call_next):
    """Добавляет в headers ключ, если он брался из кэша."""

    with cache.detect as detector:
        response = await call_next(request)
        if request.method.lower() != 'get':
            return response
        if detector.calls:
            response.headers['X-From-Cache-keys'] = 'cached_info'
    return response


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.from_url(f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}')
    elastic.es = elastic.ElasticStorage()
    cache.setup(f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}')


@app.on_event('shutdown')
async def shutdown():
    if redis.redis:
        await redis.redis.close()

    if elastic.es:
        await elastic.es.close()

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=config.LOG_LEVEL,
    )
