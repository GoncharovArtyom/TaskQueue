from typing import Optional
from uuid import UUID

import gino

from . import entities


class TaskProvider:
    """
    Класс для доступа к задачам.
    """

    def __init__(self, engine: gino.GinoEngine):
        """
        :param engine: объект для выполнения запросов к БД.
        """

        self._engine = engine

    async def get(self, identifier: UUID) -> Optional[entities.Task]:
        """
        Получение объекта по идентификатору.

        :param identifier:
        :return:
        """

        query = entities.Task.query.where(entities.Task.id == identifier)
        async with self._engine.acquire() as conn:
            task = await conn.first(query)

        return task

    async def store(self, task: entities.Task):
        """
        Сохранение задачи.

        :param task:
        :return:
        """

        query = entities.Task.insert().values(**task.to_dict())
        async with self._engine.acquire() as conn:
            await conn.status(query)

