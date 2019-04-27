import asyncio

import aio_pika
import aiohttp.web
import gino

import configs
from database import TaskProvider
from producer import Producer

task_provider: TaskProvider = None
producer: Producer = None
was_initialized: bool = False

_engine = None
_connection = None


async def initialize(app: aiohttp.web.Application):
    """
    Инициализация контекста.

    :return:
    """

    global task_provider, _engine, _connection, producer, was_initialized

    _engine = await gino.create_engine(configs.DATABASE_URI)
    task_provider = TaskProvider(_engine)

    _connection = await aio_pika.connect(configs.RABBITMQ_URI, loop=asyncio.get_running_loop())
    channel = await _connection.channel()
    await channel.declare_queue(configs.TASK_Q_NAME, durable=True)
    producer = Producer(channel.default_exchange)

    was_initialized = True


async def finalize(app: aiohttp.web.Application):
    """
    Освобождение ресурсов.

    :param app:
    :return:
    """

    global _engine, connection

    await _engine.close()
    await _connection.close()
