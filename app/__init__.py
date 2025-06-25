from litestar import Litestar
from app.routes import routes
from app.dependencies import dependencies
from app.config import Config
# from app.middleware.jwt import JWTAuthenticationMiddleware


app = Litestar(
    route_handlers=routes,
    dependencies=dependencies,
    debug=Config.DEBUG,
    # middleware=[JWTAuthenticationMiddleware]
)