from litestar import Litestar
from app.routes import routes
from app.dependencies import dependencies
from app.config import Config
# from app.middleware.jwt import JWTAuthenticationMiddleware
from app.startup import on_startup

app = Litestar(
    route_handlers=routes,
    dependencies=dependencies,
    on_startup=[on_startup],
    debug=Config.DEBUG,
    # middleware=[JWTAuthenticationMiddleware]
)