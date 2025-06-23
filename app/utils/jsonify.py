from litestar.status_codes import HTTP_200_OK
from litestar import Response

def jsonify(code: int=HTTP_200_OK, data: object="", msg: str="") -> Response:
    return Response({
        "code": code,
        "data": data,
        "msg": msg,
    })