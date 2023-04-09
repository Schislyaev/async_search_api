import json
from collections.abc import Generator

import config
from elasticsearch import Elasticsearch, ElasticsearchException, helpers
from redis_storage import State
from table import ElasticIndex
from util import log

# logging setup
logger = log(__name__)


class ESLoader:
    def __init__(self, index: str):
        self.index = index

        try:
            with open(f'{index}_index.json') as file:
                self.settings = json.load(file)
        except Exception as er:
            logger.exception(er)
            logger.error('Не удалось загрузить схему для ES')
            raise er

        self.es = self.connect_elasticsearch()
        self.create_index()

    @staticmethod
    def connect_elasticsearch():
        _es = None
        try:
            _es = Elasticsearch(
                [{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}],
            )
            if _es.ping():
                logger.info('Connected elastic')
            else:
                raise ElasticsearchException
        except ElasticsearchException as er:
            logger.exception(er)
            raise er
        return _es

    def create_index(self) -> bool:
        created = False

        try:
            if not self.es.indices.exists(self.index):
                self.es.indices.create(index=self.index, body=self.settings)
                logger.info('Index created')
                created = True
            else:
                logger.info('Already exists')
        except ElasticsearchException as er:
            logger.exception(er)
        return created

    @staticmethod
    def generate_actions(list_of_data: list[ElasticIndex]) -> Generator:
        """Func for bulk process."""

        for elem in list_of_data:
            yield elem.to_elastic()

    def load(self, state: State, record: list):

        try:
            helpers.bulk(
                client=self.es,
                index=self.index,
                actions=self.generate_actions(record),
            )

            # отслеживаем дату - кладем ее в редис
            state.set_state(self.index, record[-1].modified)
            logger.info(f'Сохранили в Redis состояние {state.get_state("modified")}')
        except Exception as er:
            logger.exception(er)
            logger.error('Не удалось загрузить данные в ES')

    def close(self):
        """Func for correct closing."""
        try:
            self.es.transport.connection_pool.close()
            logger.info('Соединение с ES закрыто')
        except Exception as er:
            logger.exception(er)
            logger.error('Проблема с закрытием соединения ES')
