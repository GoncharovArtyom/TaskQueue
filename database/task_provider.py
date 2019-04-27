import contextlib
from typing import Optional, List
from uuid import UUID

import gino
from sqlalchemy.sql.elements import BinaryExpression

from . import entities


class TaskProvider:
    """
    Класс для доступа к задачам.
    """

    def __init__(self, engine: gino.GinoEngine):
        """
        :param engine: объект для выполнения запросов к БД.
        """

        self._engine: gino.GinoEngine = engine
        self._conn: Optional[gino.GinoConnection] = None

    async def get(self, identifier: UUID) -> Optional[entities.Task]:
        """
        Получение задачи по идентификатору.

        :param identifier:
        :return:
        """

        query = entities.Task.query.where(entities.Task.id == identifier)
        if self._conn is not None:
            task = await self._conn.first(query)
        else:
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
        if self._conn is not None:
            await self._conn.status(query)
        else:
            async with self._engine.acquire() as conn:
                await conn.status(query)

    async def find(self, expression: BinaryExpression) -> List[entities.Task]:
        """
        Получение списка всех задач, которые удовлетворяют условию.

        :param expression:
        :return:
        """

        query = entities.Task.query.where(expression)
        if self._conn is not None:
            tasks = await self._conn.all(query)
        else:
            async with self._engine.acquire() as conn:
                tasks = await conn.all(query)

        return tasks

    async def update(self, task: entities.Task):
        """
        Обновление задачи.

        :param task:
        :return:
        """

        query = entities.Task.update.values(**task.to_dict()).where(entities.Task.id == task.id)
        if self._conn is not None:
            await self._conn.status(query)
        else:
            async with self._engine.acquire() as conn:
                await conn.status(query)

    @contextlib.asynccontextmanager
    async def transaction(self):
        """
        Менеджер контекста для использования транзакций.

        :return:
        """

        async with self._engine.acquire() as conn, conn.transaction():
            self._conn = conn

            yield

            self._conn = None


