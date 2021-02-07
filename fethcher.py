import os
import sys
from signal import signal, SIGQUIT, SIGINT
from time import sleep
from typing import Any, Optional

import requests
from redis import Redis

import weather

CITY_ID_STHLM = 2673722
CITY_ID_SOLNA = 2675397
CITY_CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?" \
                           "id={id}&appid={key}&units=metric"


class ArgNotProvidedException(Exception):
    cli_idx: int
    env_var: str

    def __init__(self, cli_idx: int, env_var: str):
        self.cli_idx = cli_idx
        self.env_var = env_var

    def __str__(self):
        return f"Arg at index {self.cli_idx} is not provided. Could be env var {self.env_var}"


def read_arg(cli_idx: int, env_name: str, default: Optional[Any] = None) -> str:
    value: Any
    if len(sys.argv) > cli_idx:
        value = sys.argv[cli_idx]
    else:
        value = os.getenv(env_name)

    if value is not None:
        return value

    if default is not None:
        return default

    raise ArgNotProvidedException(cli_idx, env_name)


def quit_handler(signum, frame):
    print()
    print('Good bye')
    sys.exit(0)


if __name__ == '__main__':
    apiKey: str = read_arg(1, 'API_KEY')
    period_sec: int = int(read_arg(2, 'PERIOD_SEC', -1))

    place_id = CITY_ID_SOLNA
    url = CITY_CURRENT_WEATHER_URL.format(id=place_id, key=apiKey)

    signal(SIGINT, quit_handler)
    signal(SIGQUIT, quit_handler)

    if period_sec > 0:
        print(f"Fetching weather data every {period_sec} seconds. Use Ctrl+D to quit...\n")

    while True:
        resp = requests.get(url)
        resp.raise_for_status()

        json = resp.json()
        try:
            state: weather.WeatherState = weather.from_api(json)
            print(weather.as_readable(state))
        except Exception as e:
            print(f"Cannot parse following json:\n{json}", file=sys.stderr)
            raise e

        if period_sec > 0:
            sleep(period_sec)
        else:
            break
