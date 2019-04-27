import enum
import functools
import json
from datetime import datetime, timedelta
from uuid import UUID

from . import web


def json_response(async_handler):
    """
    Декоратор для создания ответа в формате json.

    :param async_handler:
    :return:
    """

    @functools.wraps(async_handler)
    async def wrapper(*args, **kwargs):
        code, data = await async_handler(*args, **kwargs)

        return web.json_response(data, status=code, dumps=lambda o: json.dumps(o, cls=Encoder))

    return wrapper


class Encoder(json.JSONEncoder):
    """
    Кодирование дат, типов и идентификаторов в json
    """

    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, enum.Enum):
            return o.value
        elif isinstance(o, timedelta):
            return str(o)
        else:
            super().default(o)
