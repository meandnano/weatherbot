import os
import sys
from time import struct_time, gmtime, asctime

import requests

CITY_ID_STHLM = 2673722
CITY_ID_SOLNA = 2675397
CITY_CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?" \
                           "id={id}&appid={key}&units=metric"


class WeatherState:
    place_name: str
    weather_desc: str
    temp: float
    temp_feels_like: float
    pressure: int
    humidity: int
    cloud: int
    wind_speed: float
    when: struct_time

    def __init__(self, json_response: dict):
        self.place_name = json_response['name']
        self.weather_desc = json_response['weather'][0]['description']
        self.temp = json_response['main']['temp']
        self.temp_feels_like = json_response['main']['feels_like']
        self.pressure = json_response['main']['pressure']
        self.humidity = json_response['main']['humidity']
        self.cloud = json_response['clouds']['all']
        self.wind_speed = json_response['wind']['speed']
        self.when = gmtime(json_response['dt'])

    def __printable_time(self) -> str:
        return asctime(self.when)

    def __str__(self):
        return f"""Weather in {self.place_name} on {self.__printable_time()} is {self.weather_desc},
it is now {round(self.temp)}°C that feels like {round(self.temp_feels_like)}°C because wind speed is {round(self.wind_speed)} m/sec
Clouds are taking {self.cloud}% of the sky
Pressure is {self.pressure} hPa and humidity is {self.humidity}%"""


if __name__ == '__main__':
    apiKey: str
    if len(sys.argv) > 1:
        apiKey = sys.argv[1]
    else:
        apiKey = os.getenv('API_KEY')

    if not apiKey:
        print("No api key provided, pass it as the first arg or in API_KEY env var", file=sys.stderr)
        exit(1)

    resp = requests.get(CITY_CURRENT_WEATHER_URL.format(id=CITY_ID_SOLNA, key=apiKey))
    resp.raise_for_status()

    json = resp.json()
    print(json)
    print(WeatherState(json))
