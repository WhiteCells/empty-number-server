from litestar import Router
from app.controllers.user_controller import UserController
from app.controllers.empty_number_controller import EmptyNumberController

# user_router = Router(path="/api", route_handlers=[UserController])

routes = [
    Router(path="/api", route_handlers=[EmptyNumberController]),
    Router(path="/api/users", route_handlers=[UserController])
]