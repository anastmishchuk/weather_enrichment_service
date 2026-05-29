FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./

COPY backend/ ./backend/

WORKDIR /app/backend

RUN pip install --no-cache-dir /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
