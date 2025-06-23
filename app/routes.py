from litestar import Router
from app.controllers.dialplan import DialplanController
from app.controllers.account import AccountController
from app.controllers.api import ApiController

routes = [
    Router(path="/api", route_handlers=[
        DialplanController,
        AccountController,
    ]),
    Router(path="/voip", route_handlers=[
        ApiController,
    ]),
]
