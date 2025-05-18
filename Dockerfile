FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y python3-dev

RUN pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml poetry.lock /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . /code/

EXPOSE 8000

