import sys
from signal import signal, SIGQUIT, SIGINT, SIGTERM
from time import sleep

import requests
from defaultenv import env
from redis import Redis

import weather
from env_support import require_env

CITY_ID_STHLM = 2673722
CITY_ID_SOLNA = 2675397
CITY_CURRENT_WEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "id={id}&appid={key}&units=metric"
)


def quit_handler(signum, frame):
    print()
    print("Good bye")
    sys.exit(0)


if __name__ == "__main__":
    apiKey: str = require_env(env("API_KEY"), "API_KEY")
    period_sec: int = int(env("PERIOD_SEC", -1))
    redis_host: str = env("REDIS_HOST", "localhost")
    redis_port: int = int(env("REDIS_PORT", 6379))
    redis_db: int = int(env("REDIS_DB", 0))

    place_id = CITY_ID_SOLNA
    url = CITY_CURRENT_WEATHER_URL.format(id=place_id, key=apiKey)

    signal(SIGINT, quit_handler)
    signal(SIGQUIT, quit_handler)
    signal(SIGTERM, quit_handler)

    print()
    print(f"Connecting to Redis at {redis_host}:{redis_port} (db={redis_db})...")
    redis = Redis(host=redis_host, port=redis_port, db=redis_db)
    redis.ping()

    if period_sec > 0:
        print(
            f"Fetching weather data every {period_sec} seconds. Use Ctrl+D to quit...\n"
        )

    while True:
        resp = requests.get(url)
        resp.raise_for_status()

        json = resp.json()
        try:
            state: weather.WeatherState = weather.from_api(json)
            redis.hset(name=place_id, mapping=state)
            print(weather.as_readable(state))
        except Exception as e:
            print(f"Cannot parse following json:\n{json}", file=sys.stderr)
            raise e

        if period_sec > 0:
            sleep(period_sec)
        else:
            break
