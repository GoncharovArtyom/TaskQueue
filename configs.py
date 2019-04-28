import os

DATABASE_URI = os.environ.get("DATABASE_URI")
RABBITMQ_URI = os.environ.get("RABBITMQ_URI")
TASK_Q_NAME = "task_q"

assert DATABASE_URI, "Не задана переменная окружения DATABASE_URI для подключения к БД."
assert RABBITMQ_URI, "Не задана переменная окружения RABBITMQ_URI для подключения к очереди."
