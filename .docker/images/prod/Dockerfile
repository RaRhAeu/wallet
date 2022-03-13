FROM python:3.9-slim

RUN apt update && apt install gcc -y

RUN pip install -U pip && pip install poetry

COPY ./poetry.lock ./pyproject.toml /

COPY ./wallet /wallet

RUN poetry install --no-dev
