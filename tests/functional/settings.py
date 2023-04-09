from pydantic import BaseSettings


class TestSettings(BaseSettings):
    es_host: str = '127.0.0.1'
    es_port: int = 9200
    redis_host: str = '127.0.0.1'
    redis_port: int = 6379
    service_url: str = '127.0.0.1'
    service_port: int = 8000

    class Config:
        env_file = '.env.test'
        env_file_encoding = 'utf-8'


test_settings = TestSettings()
