from datetime import datetime
from typing import TypedDict, Dict, Optional

from pytz import utc, timezone


class WeatherState(TypedDict):
    place_name: str
    weather_desc: str
    temp: float
    temp_feels_like: float
    pressure: int
    humidity: int
    cloud: int
    wind_speed: float
    when: float


def as_readable(weather: WeatherState, tz_name: Optional[str] = None):
    weather_datetime = datetime.fromtimestamp(weather["when"], tz=utc)

    fmt = "%d %b %Y %H:%M %Z"

    if tz_name is not None:
        weather_datetime = weather_datetime.astimezone(timezone(tz_name))

    time_repr: str = weather_datetime.strftime(fmt)

    return f"""Weather in {weather['place_name']} on {time_repr} is {weather['weather_desc']},
it is now {round(weather['temp'])}°C that feels like {round(weather['temp_feels_like'])}°C because wind speed is {round(weather['wind_speed'])} m/sec
Clouds are taking {weather['cloud']}% of the sky
Pressure is {weather['pressure']} hPa and humidity is {weather['humidity']}%"""


def from_api(json_response: dict) -> WeatherState:
    return WeatherState(
        place_name=json_response["name"],
        weather_desc=json_response["weather"][0]["description"],
        temp=json_response["main"]["temp"],
        temp_feels_like=json_response["main"]["feels_like"],
        pressure=json_response["main"]["pressure"],
        humidity=json_response["main"]["humidity"],
        cloud=json_response["clouds"]["all"],
        wind_speed=json_response["wind"]["speed"],
        when=json_response["dt"],
    )


def from_dto(redis_dto: Dict[bytes, bytes]) -> WeatherState:
    return WeatherState(
        place_name=redis_dto.get(b"place_name").decode("utf-8"),
        weather_desc=redis_dto.get(b"weather_desc").decode("utf-8"),
        temp=float(redis_dto.get(b"temp")),
        temp_feels_like=float(redis_dto.get(b"temp_feels_like")),
        pressure=int(redis_dto.get(b"pressure")),
        humidity=int(redis_dto.get(b"humidity")),
        cloud=int(redis_dto.get(b"cloud")),
        wind_speed=float(redis_dto.get(b"wind_speed")),
        when=float(redis_dto.get(b"when")),
    )
