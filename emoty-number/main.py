"""
实现一个回调的服务，用于接收文件，
返回给后端提供的接口
"""

from litestar import Litestar, post
from litestar.datastructures import UploadFile
from litestar.response import Response
from typing import List


@post("/wav_file")
async def file_callback(files: List[UploadFile]) -> Response:
    """
    接收文件上传的回调接口
    """
    result = []
    for file in files:
        content = await file.read()  # 读取文件内容
        result.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content)
        })

    return Response(result)


app = Litestar(route_handlers=[file_callback])
