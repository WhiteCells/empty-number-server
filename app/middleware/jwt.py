from typing import Any, Awaitable, Callable, Dict, Optional, Union
from jose import jwt, JWTError
from litestar.middleware import MiddlewareProtocol
from litestar.types import ASGIApp, Receive, Scope, Send
from litestar.exceptions import NotAuthorizedException
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.config import Config
from app.models.user_model import User

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=Config.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise NotAuthorizedException("Invalid token")
        # raise jsonify(status_code=401, msg="Invalid token")


# JWT 认证中间件
class JWTAuthenticationMiddleware(MiddlewareProtocol):
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.exclude_paths = {"/login", "/docs", "/openapi.json"}  # 排除不需要认证的路径

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # if scope["type"] != "http":
        #     await self.app(scope, receive, send)
        #     return

        # 检查是否为排除的路径
        path = scope["path"]
        if path in self.exclude_paths:
            await self.app(scope, receive, send)
            return

        try:
            # 从请求头中获取令牌
            headers = dict(scope["headers"])
            auth_header = headers.get(b"authorization")
            if not auth_header or not auth_header.startswith(b"Bearer "):
                raise NotAuthorizedException("Authorization header missing or invalid")
                # raise jsonify(code=401, msg="Authorization header missing or invalid")

            token = auth_header.split(b" ")[1].decode("utf-8")
        
            # 验证并解析令牌
            payload = decode_token(token)
            
            # 从令牌中提取用户信息并注入到请求中
            user_id = payload.get("sub")
            if not user_id:
                raise NotAuthorizedException("Invalid authentication credentials")
                # raise jsonify(code=401, msg="Invalid authentication credentials")
            
            # 这里可以根据需要从数据库或其他存储中获取完整的用户对象
            user = User(id=user_id, username=payload.get("username"), role=payload.get("role"))
            
            # 将用户信息存储在 scope 中，以便后续处理程序可以访问
            scope["user"] = user
            
        except NotAuthorizedException as e:
            # 直接返回异常
            from litestar.response import Response
            from litestar.status_codes import HTTP_401_UNAUTHORIZED
            response = Response(
                content={"detail": e.detail},
                status_code=HTTP_401_UNAUTHORIZED,
                headers=scope.get("headers", {})
            )
            await response(scope, receive, send)
            return
            
        await self.app(scope, receive, send)

