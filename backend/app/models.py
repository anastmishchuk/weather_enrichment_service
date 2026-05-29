from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    snapshots: Mapped[list["WeatherSnapshot"]] = relationship(
        "WeatherSnapshot", back_populates="city", order_by="WeatherSnapshot.fetched_at.desc()"
    )


class WeatherSnapshot(Base):
    __tablename__ = "weather_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id"), nullable=False)
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    city: Mapped["City"] = relationship("City", back_populates="snapshots")
