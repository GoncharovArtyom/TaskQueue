import os

DATABASE_URI = os.environ.get("DATABASE_URI", "postgresql://postgres:1234@localhost:5432/task_queue")

assert DATABASE_URI, "Не задана переменная окружения DATABASE_URI для подключения к БД."
