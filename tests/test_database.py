import pytest

from uuid import uuid4
from database import TaskProvider, entities


@pytest.mark.asyncio
async def test_task_get_none(engine):

    task_provider = TaskProvider(engine)

    task = await task_provider.get(uuid4())

    assert task is None


@pytest.mark.asyncio
async def test_task_store(engine, new_task1):
    task_provider = TaskProvider(engine)

    await task_provider.store(new_task1)

    query = entities.Task.query.where(entities.Task.id == new_task1.id)
    async with engine.acquire() as conn:
        task_from_db = await conn.first(query)

    assert task_from_db is not None


@pytest.mark.asyncio
async def test_task_find(engine, new_task1, new_task2):
    task_provider = TaskProvider(engine)

    await task_provider.store(new_task1)
    await task_provider.store(new_task2)

    tasks_from_db = await task_provider.find(entities.Task.id.in_([new_task1.id, new_task2.id]))

    assert len(tasks_from_db) == 2

@pytest.mark.asyncio
async def test_task_update(engine, new_task1):
    task_provider = TaskProvider(engine)
    await task_provider.store(new_task1)

    new_task1.status = entities.TaskStatusEnum.running
    await task_provider.update(new_task1)

    task1_from_db = await task_provider.get(new_task1.id)

    assert task1_from_db.status is entities.TaskStatusEnum.running
