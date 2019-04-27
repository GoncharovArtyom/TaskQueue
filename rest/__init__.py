from aiohttp import web

from . import context

app = web.Application()
app.on_startup.append(context.initialize)

routes = web.RouteTableDef()
from . import endpoints  # Чтобы при импорте web исполнялся модуль endpoints

app.add_routes(routes)
