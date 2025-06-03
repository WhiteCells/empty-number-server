from litestar import Controller, get, post, Request
from litestar.exceptions import HTTPException
from typing import List, Dict
import uuid
import time
from app.models.user_model import User
from app.utils.jsonify import jsonify
from app.utils.types import JsonifyReturnType


class EmptyNumberController(Controller):

    @get("/notify")
    async def get_client_id(self, request: Request) -> JsonifyReturnType:
        # 解析请求ip
        ip = request.client.host
        print(ip)
        client_id = str(uuid.uuid4())
        return jsonify(data={
                "clientId": client_id
            })


    @get("/dialplan/{clientId:str}")
    async def get_dial_plan(self, clientId: str) -> JsonifyReturnType:
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
    async def get_accounts(self, clientId: str, threadsNum: int) -> JsonifyReturnType:
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
    async def heartbeat(self, clientId: str) -> JsonifyReturnType:
        timestamp = str(int(time.time()))
        return jsonify(data={
                "timestamp": timestamp
            })


    @get("/status/{clientId:str}")
    async def submit_status(self, clientId: str, status: str, extensionNum: str, phoneNum: str) -> JsonifyReturnType:
        valid_statuses = ["during", "call", "idle", "unregistered"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status")
        timestamp = str(int(time.time()))
        return jsonify(data={
                "timestamp": timestamp
            })


    @post("/dial_wav/{clientId:str}")
    async def upload_audio(self, clientId: str, request: Request) -> JsonifyReturnType:
        data = await request.form()
        file_name = data.get("file_name")
        extensionNum = data.get("extensionNum")
        phone = data.get("phone")
        timestamp = str(int(time.time()))
        return jsonify(data={
                "timestamp": timestamp
            })
