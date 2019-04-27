import asyncio

import aio_pika
import gino

import configs
from database import TaskProvider

task_provider: TaskProvider = None
queue: aio_pika.Queue = None

connection: aio_pika.Connection = None

was_initialized: bool = False


async def initialize():
    """
    Инициализация контекста.

    :return:
    """

    global task_provider, queue, connection, was_initialized

    _engine = await gino.create_engine(configs.DATABASE_URI)
    task_provider = TaskProvider(_engine)

    connection = await aio_pika.connect(configs.RABBITMQ_URI, loop=asyncio.get_running_loop())
    channel = await connection.channel()
    queue = await channel.declare_queue(configs.TASK_Q_NAME, durable=True)

    was_initialized = True
