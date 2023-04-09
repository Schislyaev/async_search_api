import logging
import os

from pydantic import BaseSettings


class AppConfig(BaseSettings):
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'Read-only API для онлайн-кинотеатра')
    PROJECT_DESCRIPTION = os.getenv('PROJECT_DESCRIPTION',
                                    'Информация о фильмах, жанрах и людях, участвовавших в создании произведения')
    PROJECT_VERSION = os.getenv('PROJECT_VERSION', '1.0.0')
    REDIS_HOST = os.getenv('redis_host', '127.0.0.1')
    REDIS_PORT = int(os.getenv('redis_port', 6379))
    REDIS_CACHE_TIMEOUT = 60 * 5
    ELASTIC_HOST = os.getenv('es_host', '127.0.0.1')
    ELASTIC_PORT = int(os.getenv('es_port', 9200))
    LOG_LEVEL = (os.getenv('LOGGING', logging.DEBUG))

    @property
    def elastic_connection_string(self):
        return f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'

    class Config:
        use_enum_values = True


config: AppConfig = AppConfig(_env_file_encoding='utf-8')
