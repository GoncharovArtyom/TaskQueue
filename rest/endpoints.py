from uuid import UUID

from . import routes, web
from . import context
from .utils import json_response
from database import entities


@routes.post("/tasks")
@json_response
async def create_task(request):
    """
    Создание задачи.

    :param request:
    :return:
    """

    task = entities.Task.make()
    async with context.task_provider.transaction():
        await context.task_provider.store(task)
        await context.producer.put(task.id)

    return 201, task.to_dict()


@routes.get("/tasks/{id}")
@json_response
async def get_task(request):
    """
    Получение информации о задаче.

    :param request:
    :return:
    """

    identifier = request.match_info["id"]

    try:
        identifier = UUID(identifier)
    except Exception:
        raise web.HTTPNotFound

    task = await context.task_provider.get(identifier)

    if task is None:
        raise web.HTTPNotFound

    return 200, task.to_dict()
