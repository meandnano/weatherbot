import pytest
from redis import Redis

from app import weather


@pytest.fixture(scope="module")
def redis_conn() -> Redis:
    instance = Redis(host='redis', port=6379, db=0)
    yield instance
    instance.close()


@pytest.fixture
def redis_mem(redis_conn: Redis, request) -> Redis:
    """Removes all contents of the current DB after each test"""

    def finalizer():
        redis_conn.flushdb()

    request.addfinalizer(finalizer)

    return redis_conn


def test_from_dto_succeeds(redis_mem: Redis):
    state: weather.WeatherState = {
        'place_name': "New Ark",
        'weather_desc': 'cloudy',
        'temp': 18.5,
        'temp_feels_like': 11.6,
        'pressure': 108,
        'humidity': 56,
        'cloud': 80,
        'wind_speed': 1.1,
        'when': 0.0
    }

    redis_mem.hset(name=1, mapping=state)
    read = redis_mem.hgetall(1)

    assert state == weather.from_dto(read)
