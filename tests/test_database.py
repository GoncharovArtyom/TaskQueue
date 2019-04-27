import pytest

from uuid import uuid4
from database import TaskProvider, entities


@pytest.mark.asyncio
async def test_task_provider(engine):

    task_provider = TaskProvider(engine)

    task = await task_provider.get(uuid4())

    assert task is None


@pytest.mark.asyncio
async def test_task_store(engine, new_task):
    task_provider = TaskProvider(engine)

    await task_provider.store(new_task)

    query = entities.Task.query.where(entities.Task.id == new_task.id)
    async with engine.acquire() as conn:
        task_from_db = await conn.first(query)

    assert task_from_db is not None