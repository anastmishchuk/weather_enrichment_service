import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://weather:weather@db:5432/weather"
    redis_url: str = "redis://redis:6379/0"
    openweather_api_key: str | None

    class Config:
        env_file = ".env"


settings = Settings(openweather_api_key=os.environ.get("OPENWEATHER_API_KEY"))
