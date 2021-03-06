from app.weather import WeatherState, as_readable


def test_as_readable_works_when_default_tz():
    w: WeatherState = {
        "place_name": "New Ark",
        "weather_desc": "cloudy",
        "temp": 18.5,
        "temp_feels_like": 11.6,
        "pressure": 108,
        "humidity": 56,
        "cloud": 80,
        "wind_speed": 1.1,
        "when": 0.0,
    }

    assert (
        as_readable(w)
        == """Weather in New Ark on 01 Jan 1970 00:00 UTC is cloudy,
it is now 18°C that feels like 12°C because wind speed is 1 m/sec
Clouds are taking 80% of the sky
Pressure is 108 hPa and humidity is 56%"""
    )


def test_as_readable_works_when_specific_tz():
    w: WeatherState = {
        "place_name": "New Ark",
        "weather_desc": "cloudy",
        "temp": 18.5,
        "temp_feels_like": 11.6,
        "pressure": 108,
        "humidity": 56,
        "cloud": 80,
        "wind_speed": 1.1,
        "when": 0.0,
    }

    assert (
        as_readable(w, "CET")
        == """Weather in New Ark on 01 Jan 1970 01:00 CET is cloudy,
it is now 18°C that feels like 12°C because wind speed is 1 m/sec
Clouds are taking 80% of the sky
Pressure is 108 hPa and humidity is 56%"""
    )
