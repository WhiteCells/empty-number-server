from litestar import Controller, get, post, Request, Response
from litestar.exceptions import HTTPException
from litestar.datastructures import UploadFile
from litestar.params import Body
from typing import List, Dict
import uuid
import time
from app.utils.jsonify import jsonify

class EmptyNumberController(Controller):

    @get("/notify")
    async def get_client_id(self, request: Request) -> Response:
        # 解析请求ip
        ip = request.client.host
        print(ip)
        client_id = str(uuid.uuid4())
        return jsonify(data={
                "clientId": client_id
            })


    @get("/dialplan/{clientId:str}")
    async def get_dial_plan(self, clientId: str) -> Response:
        # 这里可以根据 clientId 从数据库获取拨号计划
        dialplans = [
            {
                "phoneNum": "1xxxxxxxxxx"
            }
        ]
        return jsonify(data={
                "dialplans": dialplans
            })


    @get("/accounts/{clientId:str}")
    async def get_accounts(self, clientId: str, threadsNum: int) -> Response:
        # 获取分机账号列表，这里可以根据 clientId 和 threadsNum 从数据库获取账号列表
        accounts = [
            {
                "user": "xxx",
                "password": "xxxx",
                "host": "xxx"
            }
        ] * threadsNum
        return jsonify(data={
                "accounts": accounts
            })


    @post("/heartbeat/{clientId:str}")
    async def heartbeat(self, clientId: str) -> Response:
        timestamp = str(int(time.time()))
        return jsonify(data={
                "timestamp": timestamp
            })


    @get("/status/{clientId:str}")
    async def submit_status(self, clientId: str, status: str, extensionNum: str, phoneNum: str) -> Response:
        valid_statuses = ["during", "call", "idle", "unregistered"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status")
        timestamp = str(int(time.time()))
        return jsonify(data={
                "timestamp": timestamp
            })


    @post("/dial_wav/{clientId:str}")
    async def upload_audio(self, clientId: str, request: Request) -> Response:
        data = await request.form()
        file_name = data.get("file_name")
        extensionNum = data.get("extensionNum")
        phone = data.get("phone")
        timestamp = str(int(time.time()))
        return jsonify(data={
                "timestamp": timestamp
            })


    @post("/upload_dialplan_file")
    async def upload_dialplan_file(self, request: Request) -> Response:
        """
        Litestar 限制单文件上传大小为 1 MB
        todo: 后续改为前端分块后端合并
        流式读取内容，使用 pandas 读取内容

        格式:
        dialplan
        18920201010
        18020201010
        将计划输入
        """
        form = await request.form()
        file = form.get("file")
        if not isinstance(file, UploadFile):
            return {"error": "file not found or invalid"}

        content = await file.read()
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
        }
    

    @post("/upload_multiple")
    async def upload_multiple(self, request: Request) -> Response:
        """
        添加的文件为 csv 格式，使用 pandas 读取内容
        添加到数据库
        """
        form = await request.form()
        files = form.getall("files")
        results = []

        for file in files:
            if not isinstance(file, UploadFile):
                continue
            content = await file.read()
            results.append({
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content),
            })

        return {"files": results}
