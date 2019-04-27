from gino import Gino

db = Gino()

from . import entities  # Чтобы при импорте db исполнялся модуль entities
