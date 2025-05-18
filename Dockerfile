FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y python3-dev build-essential

RUN pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml poetry.lock /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi --with dev

COPY . /code/

EXPOSE 8000
