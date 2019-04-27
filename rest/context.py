import asyncio
import logging

import aio_pika
import aiohttp.web
import gino
from aiologger.formatters.json import FUNCTION_NAME_FIELDNAME
from aiologger.loggers.json import JsonLogger

import configs
from database import TaskProvider
from producer import Producer

task_provider: TaskProvider = None
producer: Producer = None
logger = None
was_initialized: bool = False

_db_engine = None
_rmq_connection_pool = None
_rmq_channel_pool = None


async def _get_connection():
    return await aio_pika.connect_robust(configs.RABBITMQ_URI)


async def _get_channel() -> aio_pika.Channel:
    async with _rmq_connection_pool.acquire() as connection:
        return await connection.channel()


async def initialize(app: aiohttp.web.Application):
    """
    Инициализация контекста.

    :return:
    """

    global task_provider, _db_engine, _rmq_connection_pool, _rmq_channel_pool, \
        producer, was_initialized, logger

    _db_engine = await gino.create_engine(configs.DATABASE_URI)
    task_provider = TaskProvider(_db_engine)

    loop = asyncio.get_running_loop()
    _rmq_connection_pool = aio_pika.pool.Pool(_get_connection, loop=loop)
    _rmq_channel_pool = aio_pika.pool.Pool(_get_channel, loop=loop)

    async with _rmq_channel_pool.acquire() as channel:
        await channel.declare_queue(configs.TASK_Q_NAME, durable=True)

    producer = Producer(_rmq_channel_pool)

    logger = JsonLogger.with_default_handlers(
        level=logging.DEBUG,
        exclude_fields=[FUNCTION_NAME_FIELDNAME,
                        'file_path',
                        'line_number']
    )

    was_initialized = True

