import asyncio
import os
import uuid

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from app.models import EventModel
from main import app


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["app.models", "aerich.models"]},
        _create_db=create_db
    )
    if create_db:
        print(f"Database created! {db_url = }")
    if schemas:
        await Tortoise.generate_schemas(safe=True)
        print("Success to generate schemas")


async def init(db_url: str = os.environ.get("TORTOISE_TEST_DB")):
    await init_db(db_url, True, True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()


@pytest.mark.asyncio
async def test():
    await EventModel.create(name=f'name-{uuid.uuid4().hex[:4]}')
    assert await EventModel.all().count() == 1
