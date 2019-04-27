from typing import Union
from uuid import UUID

import aio_pika

import configs


class Producer:
    """
    Класс для записи сообщений в очередь.
    """

    def __init__(self, channel_pool: aio_pika.pool.Pool):

        self._channel_pool = channel_pool

    async def put(self, identifier: Union[UUID, str]):
        """
        Отправка идентификатора задачи в очередь.

        :param identifier:
        :return:
        """
        data = str(identifier).encode()

        message = aio_pika.Message(
            data,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        async with self._channel_pool.acquire() as channel:
            await channel.default_exchange.publish(message, routing_key=configs.TASK_Q_NAME)







