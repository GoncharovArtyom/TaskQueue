import enum
from uuid import uuid4

import sqlalchemy
from sqlalchemy.dialects import postgresql

from . import db
from datetime import datetime


class TaskStatusEnum(enum.Enum):
    """
    Возможные статусы задач.
    """

    in_queue = "in_queue"  # задача поставлена в очередь на выполнение
    running = "running"  # задача выполняется
    completed = "completed"  # задача выполнена


class Task(db.Model):
    """
    Сущность, соответствующая таблице tasks.
    """

    __tablename__ = "tasks"

    id = db.Column(postgresql.UUID, primary_key=True)
    status = db.Column(sqlalchemy.Enum(TaskStatusEnum), nullable=False)
    create_time = db.Column(sqlalchemy.DateTime, nullable=False)
    start_time = db.Column(sqlalchemy.DateTime)
    execution_time = db.Column(sqlalchemy.DateTime)

    @classmethod
    def make(cls):
        """
        Создание задачи: задается идентификатор, статус и время создания.

        :return:
        """

        task = cls()

        task.id = uuid4()
        task.status = TaskStatusEnum.in_queue
        task.create_time = datetime.now()

        return task
