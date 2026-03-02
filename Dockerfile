FROM python:3.13-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY . /app

RUN pip install --no-cache-dir uv

RUN uv sync --no-dev --frozen
