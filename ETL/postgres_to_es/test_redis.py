from redis_storage import RedisStorage, State


class FakeRedis:
    def __init__(self):
        self.data = {}

    def get(self, name):
        return self.data.get(name)

    def set(self, name, value):
        self.data[name] = value


def test_get_empty_state():
    redis_adapter = FakeRedis()
    storage = RedisStorage(redis_adapter)
    state = State(storage)

    assert state.get_state('key') is None


def test_save_new_state():
    redis_adapter = FakeRedis()
    storage = RedisStorage(redis_adapter)
    state = State(storage)

    state.set_state('key', 123)

    assert redis_adapter.data == {'data': '{"key": 123}'}


def test_retrieve_existing_state():
    redis_adapter = FakeRedis()
    redis_adapter.data = {'data': '{"key": 10}'}
    storage = RedisStorage(redis_adapter)
    state = State(storage)

    assert state.get_state('key') == 10


def test_save_state_and_retrieve():
    redis_adapter = FakeRedis()
    storage = RedisStorage(redis_adapter)
    state = State(storage)

    state.set_state('key', 123)

    # Принудительно удаляем объекты
    del state
    del storage

    storage = RedisStorage(redis_adapter)
    state = State(storage)

    assert state.get_state('key') == 123
