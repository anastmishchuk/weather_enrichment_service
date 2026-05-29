from datetime import datetime

from pydantic import BaseModel, field_serializer


class WeatherSnapshotOut(BaseModel):
    temperature: float | None
    humidity: int | None
    description: str | None
    fetched_at: datetime

    model_config = {"from_attributes": True}

    @field_serializer("fetched_at")
    def serialize_fetched_at(self, dt: datetime) -> str:
        return dt.isoformat() + "Z"


class CityCreate(BaseModel):
    name: str


class CityOut(BaseModel):
    id: int
    name: str
    created_at: datetime
    weather: WeatherSnapshotOut | None = None

    model_config = {"from_attributes": True}
