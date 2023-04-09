import backoff
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
from settings import test_settings


@backoff.on_exception(backoff.expo, ConnectionError)
def ping_es():
    es_client = Elasticsearch(hosts=test_settings.es_host, validate_cert=False, use_ssl=False)
    es_client.transport.perform_request("HEAD", "/")


if __name__ == '__main__':
    ping_es()
