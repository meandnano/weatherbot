import json

import pytest

from app import weather

"""Taken from https://openweathermap.org/current"""
resp_json = """{
  "coord": {
    "lon": -122.08,
    "lat": 37.39
  },
  "weather": [
    {
      "id": 800,
      "main": "Clear",
      "description": "clear sky",
      "icon": "01d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 282.55,
    "feels_like": 281.86,
    "temp_min": 280.37,
    "temp_max": 284.26,
    "pressure": 1023,
    "humidity": 100
  },
  "visibility": 16093,
  "wind": {
    "speed": 1.5,
    "deg": 350
  },
  "clouds": {
    "all": 1
  },
  "dt": 1560350645,
  "sys": {
    "type": 1,
    "id": 5122,
    "message": 0.0139,
    "country": "US",
    "sunrise": 1560343627,
    "sunset": 1560396563
  },
  "timezone": -25200,
  "id": 420006353,
  "name": "Mountain View",
  "cod": 200
  }"""


def test_from_api_succeeds_when_correct_json():
    expected: weather.WeatherState = {
        "place_name": "Mountain View",
        "weather_desc": "clear sky",
        "temp": 282.55,
        "temp_feels_like": 281.86,
        "pressure": 1023,
        "humidity": 100,
        "cloud": 1,
        "wind_speed": 1.5,
        "when": 1560350645.0,
    }

    json_dict: dict = json.loads(resp_json)

    assert expected == weather.from_api(json_dict)


def test_from_api_raises_when_insufficient_json():
    json_dict: dict = json.loads("{}")

    with pytest.raises(KeyError):
        weather.from_api(json_dict)
