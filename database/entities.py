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

    id = db.Column(postgresql.UUID, primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"))
    status = db.Column(sqlalchemy.Enum(TaskStatusEnum), nullable=False)
    create_time = db.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now(), nullable=False)
    start_time = db.Column(sqlalchemy.DateTime)
    execution_time = db.Column(sqlalchemy.DateTime)

