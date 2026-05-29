# Weather Enrichment Service

A web app to track cities and view their current weather data.

**Stack:** FastAPI · Celery · PostgreSQL · Redis · Angular · Docker

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [OpenWeatherMap API key](https://openweathermap.org/api)

## Setup & Run

1. Copy the example env file and set your API key:
   ```bash
   cp .env.example .env
   # edit .env and set OPENWEATHER_API_KEY=your_key_here
   ```

2. Start all services:
   ```bash
   docker-compose up
   ```

## Access

| Service  | URL                       |
| -------- | ------------------------- |
| Frontend | http://localhost:4200     |
| API docs | http://localhost:8000/docs |
