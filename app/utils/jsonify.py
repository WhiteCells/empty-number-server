from litestar.status_codes import HTTP_200_OK
from app.utils.types import JsonifyReturnType


def jsonify(code: int=HTTP_200_OK, data: object="", msg: str="") -> JsonifyReturnType:
    return {
        "code": code,
        "data": data,
        "msg": msg,
    }, code