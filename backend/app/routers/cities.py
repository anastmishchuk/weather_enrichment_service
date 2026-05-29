from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import City
from app.schemas import CityCreate, CityOut, WeatherSnapshotOut
from app.tasks import fetch_weather_task

router = APIRouter(prefix="/cities", tags=["cities"])


def _latest_snapshot(city: City) -> WeatherSnapshotOut | None:
    if not city.snapshots:
        return None
    return WeatherSnapshotOut.model_validate(city.snapshots[0])


@router.post("", response_model=CityOut, status_code=status.HTTP_201_CREATED)
def add_city(payload: CityCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(City).where(City.name == payload.name))
    if existing:
        raise HTTPException(status_code=409, detail="City already exists")

    city = City(name=payload.name)
    db.add(city)
    db.commit()
    db.refresh(city)

    fetch_weather_task.delay(city.id)

    return CityOut(id=city.id, name=city.name, created_at=city.created_at, weather=None)


@router.get("", response_model=list[CityOut])
def list_cities(db: Session = Depends(get_db)):
    cities = db.scalars(
        select(City).options(selectinload(City.snapshots)).order_by(City.created_at)
    ).all()
    return [
        CityOut(
            id=c.id,
            name=c.name,
            created_at=c.created_at,
            weather=_latest_snapshot(c),
        )
        for c in cities
    ]


@router.post("/{city_id}/refresh", status_code=status.HTTP_202_ACCEPTED)
def refresh_weather(city_id: int, db: Session = Depends(get_db)):
    city = db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City is not found")

    fetch_weather_task.delay(city_id)
    return {"detail": "Weather update queued"}
