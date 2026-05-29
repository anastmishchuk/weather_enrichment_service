from celery import Celery

from app.config import settings

celery_app = Celery("weather", broker=settings.redis_url, backend=settings.redis_url)


@celery_app.task(name="fetch_weather_task")
def fetch_weather_task(city_id: int) -> None:
    from app.database import SessionLocal
    from app.models import City, WeatherSnapshot
    from app.weather import fetch_weather

    db = SessionLocal()
    try:
        city = db.get(City, city_id)
        if not city:
            return

        weather = fetch_weather(city.name)

        snapshot = WeatherSnapshot(
            city_id=city_id,
            temperature=weather["temperature"],
            humidity=weather["humidity"],
            description=weather["description"],
        )
        db.add(snapshot)
        db.commit()
    finally:
        db.close()
