import asyncio
import logging

import aio_pika
import gino
from aiologger.formatters.json import FUNCTION_NAME_FIELDNAME
from aiologger.loggers.json import JsonLogger

import configs
from database import TaskProvider

task_provider: TaskProvider = None
queue: aio_pika.Queue = None

connection: aio_pika.Connection = None
logger = None

was_initialized: bool = False


async def initialize():
    """
    Инициализация контекста.

    :return:
    """

    global task_provider, queue, connection, was_initialized, logger

    _engine = await gino.create_engine(configs.DATABASE_URI)
    task_provider = TaskProvider(_engine)

    connection = await aio_pika.connect(configs.RABBITMQ_URI, loop=asyncio.get_running_loop())
    channel = await connection.channel()
    queue = await channel.declare_queue(configs.TASK_Q_NAME, durable=True)

    logger = JsonLogger.with_default_handlers(
        level=logging.DEBUG,
        exclude_fields=[FUNCTION_NAME_FIELDNAME,
                        'file_path',
                        'line_number']
    )

    was_initialized = True
