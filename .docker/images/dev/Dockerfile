FROM python:3.9.4-slim

RUN apt update && apt install gcc -y

RUN pip install -U pip && pip install poetry

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml ./

COPY ./wallet ./wallet
COPY ./migrations ./migrations
COPY ./tests ./tests

RUN poetry install


