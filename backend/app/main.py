from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers.cities import router as cities_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather Enrichment Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cities_router, prefix="/api")
