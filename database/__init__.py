import gino

db: gino.api.Gino = gino.Gino()

from .task_provider import TaskProvider
from . import entities  # Чтобы при импорте db исполнялся модуль entities

__all__ = ["TaskProvider", "entities"]
