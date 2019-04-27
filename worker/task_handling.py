from uuid import UUID

import aio_pika

from database import entities
from . import context
from datetime import datetime


async def handler(message: aio_pika.IncomingMessage):
    """
    Обработка задач.

    :param message:
    :return:
    """

    async with message.process():
        identifier = UUID(message.body.decode())
        task = await context.task_provider.get(identifier)

        if task is None:
            return

        start_time = datetime.now()
        task.start_time = start_time
        task.status = entities.TaskStatusEnum.running
        await context.task_provider.update(task)

        work()

        end_time = datetime.now()
        task.execution_time = end_time - start_time
        task.status = entities.TaskStatusEnum.completed
        await context.task_provider.update(task)


def work():
    """
    Задача, которую нужно выполнить.

    :return:
    """

    import time
    import random
    time.sleep(random.randint(0, 10))
