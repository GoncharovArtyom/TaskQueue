from typing import Union
from uuid import UUID

import aio_pika

import configs


class Producer:
    """
    Класс для записи сообщений в очередь.
    """

    def __init__(self, exchange: aio_pika.Exchange):

        self._exchange: aio_pika.Exchange = exchange

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

        await self._exchange.publish(message, routing_key=configs.TASK_Q_NAME)






