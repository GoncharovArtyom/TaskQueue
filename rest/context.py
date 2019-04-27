import aiohttp.web
from typing import Optional

import gino

import configs
from database import TaskProvider

task_provider: Optional[TaskProvider] = None
was_initialized: bool = False


async def initialize(app: aiohttp.web.Application):
    """
    Инициализация task_provider.

    :return:
    """

    engine = await gino.create_engine(configs.DATABASE_URI)

    global task_provider
    task_provider = TaskProvider(engine)
