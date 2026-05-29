import httpx

from app.config import settings


class WeatherAPIError(Exception):
    pass


class CityNotFoundError(WeatherAPIError):
    pass


def fetch_weather(city_name: str) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": settings.openweather_api_key, "units": "metric"}

    with httpx.Client(timeout=10) as client:
        response = client.get(url, params=params)

    if response.status_code == 404:
        raise CityNotFoundError(f"City '{city_name}' is not found in OpenWeatherMap")
    if response.status_code != 200:
        raise WeatherAPIError(f"OpenWeatherMap API error: {response.status_code}")

    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
    }
