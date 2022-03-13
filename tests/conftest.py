import asyncio
import os
from typing import Iterator

import pytest
import pytest_asyncio


from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from tortoise import Tortoise

DB_URL = "sqlite://:memory:"

os.environ.update(
    {
        "DB_URL": DB_URL,
    }
)
# flake8: noqa E402
from wallet.app import app
from wallet.settings import TORTOISE_ORM


@pytest_asyncio.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="session")
async def asgi_lifespan():
    async with LifespanManager(app, startup_timeout=30):
        yield


@pytest_asyncio.fixture(scope="function")
@pytest.mark.usefixtures('asgi_lifespan')
async def db():
    await Tortoise.init(config=TORTOISE_ORM, _create_db=True)
    await Tortoise.generate_schemas(safe=False)
    yield
    await Tortoise._drop_databases()


@pytest_asyncio.fixture(scope="function")
@pytest.mark.usefixtures('db')
async def client() -> Iterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
