import enum

import sqlalchemy
from sqlalchemy.dialects import postgresql

from . import db


class TaskStatusEnum(enum.Enum):
    """
    Возможные статусы задач.
    """

    in_queue = enum.auto()  # задача поставлена в очередь на выполнение
    running = enum.auto()  # задача выполняется
    completed = enum.auto()  # задача выполнена


class Task(db.Model):
    """
    Сущность, соответствующая таблице tasks.
    """

    __tablename__ = "tasks"

    id = db.Column(postgresql.UUID, primary_key=True)
    status = db.Column(sqlalchemy.Enum(TaskStatusEnum), nullable=False)
