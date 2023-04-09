"""
Yandex.Practicum sprint 3.
Main section

Author: Petr Schislyaev
Date: 14/11/2022
"""

import contextlib

import backoff
import config
import psycopg2
from elasticsearch import ElasticsearchException
from es_loader import ESLoader
from postgresextractor import PostgresExtractor
from psycopg2 import Error
from psycopg2.extensions import connection
from redis import ConnectionError, Redis
from redis_storage import RedisStorage, State
from util import log, sleep

# logging setup
logger = log(__name__)


class ETL:
    def __init__(self):
        self.PAGE_SIZE = config.PAGE_SIZE       # int(os.environ.get('PAGE_SIZE'))
        self.dsl = config.DSL
        self.state = self.redis_connect()

    @backoff.on_exception(
        backoff.expo,
        ConnectionError,
        logger=logger
    )
    def redis_connect(self) -> State | Exception:
        try:
            adapter = Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                db=config.REDIS_DB_NUMBER,
                decode_responses=True,
            )
            storage = RedisStorage(adapter)
            state = State(storage)
            return state
        except ConnectionError as er:
            logger.exception(er)
            raise er

    @backoff.on_exception(
        backoff.expo,
        Error,
        logger=logger
    )
    def postgres_connect(self) -> connection | Exception:
        try:
            pg = psycopg2.connect(**self.dsl)
            return pg

        except Error as er:
            logger.exception(er)
            raise er

    @backoff.on_exception(
        backoff.expo,
        ElasticsearchException,
        logger=logger
    )
    def es_connect(self, index: str) -> ESLoader | Exception:
        try:
            es = ESLoader(index)
            return es
        except ElasticsearchException as er:
            logger.exception(er)
            raise er

    @sleep(config.TIMEOUT)
    def main(self):
        indexes = config.INDEX_NAMES
        with contextlib.closing(self.postgres_connect()) as pg_conn:
            for index in indexes:
                with contextlib.closing(self.es_connect(index)) as es_conn:
                    pg = PostgresExtractor(index, pg_conn, self.state)
                    pg.extract()
                    while data := pg.cursor.fetchmany(self.PAGE_SIZE):
                        res = pg.transform(data)
                        es_conn.load(self.state, res)


def main():
    etl = ETL()
    etl.main()


if __name__ == '__main__':
    main()
