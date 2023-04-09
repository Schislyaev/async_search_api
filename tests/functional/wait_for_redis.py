import backoff
from redis import Redis
from redis.exceptions import ConnectionError
from settings import test_settings


@backoff.on_exception(backoff.expo, ConnectionError)
def ping_redis():
    redis = Redis(host=test_settings.redis_host)
    redis.execute_command('PING')


if __name__ == '__main__':
    ping_redis()
