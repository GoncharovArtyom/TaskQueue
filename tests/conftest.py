from uuid import uuid4

import pytest
import os
import gino

from database import entities


@pytest.fixture(scope="session")
def test_database_uri():

    test_database_uri = os.environ.get("TEST_DATABASE_URI")
    assert test_database_uri, "Для запуска тестов необходимо задать переменную окружения TEST_DATABASE_URI"

    return test_database_uri


@pytest.fixture
async def engine(test_database_uri):

    engine = await gino.create_engine(test_database_uri)

    yield engine

    await engine.close()


@pytest.fixture
async def new_task1(engine):

    task = entities.Task.make()

    yield task

    query = entities.Task.delete.where(entities.Task.id == task.id)
    async with engine.acquire() as conn:
        await conn.status(query)


@pytest.fixture
async def new_task2(engine):

    task = entities.Task.make()

    yield task

    query = entities.Task.delete.where(entities.Task.id == task.id)
    async with engine.acquire() as conn:
        await conn.status(query)