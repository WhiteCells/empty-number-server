import datetime
import json
from typing import AsyncGenerator
from sqlalchemy import select, delete, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.dto.dialplan import CreateDialplanDto, PutDialplanDto, CreateDialplanResponseDto
from app.models.dialplan import Dialplan, DialplanStatus
from app.models.account import Account, AccountStatus
from app.models.task import Task, TaskStatus
from app.utils.dialplan_queue import get_dialplan_queue
from app.utils.logger import logger


class DialplanRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session
        self._dialplan_queue = get_dialplan_queue()

    async def create_dialplan(self, data: CreateDialplanDto) -> tuple[dict, str]:
        task = None
        dialplans = []

        try:
            # 创建 task 实例
            task = Task(
                return_url=data.return_url,
            )
            self._db_session.add(task)
            await self._db_session.flush()
            await self._db_session.refresh(task)
            # 创建 dialplan 实例
            for phone in data.phone:
                dialplan = Dialplan(
                    phone=phone,
                    task_id=task.id,
                )
                self._db_session.add(dialplan)
                await self._db_session.flush()
                dialplans.append(CreateDialplanResponseDto.model_validate(dialplan))
                # phones.append(phone)
                # 添加进 dialplan 队列
                # self._dialplan_queue.put("dialplan", phone)
            return {
                "task_id": task.id,
                "dialplans": dialplans,
                "return_url": task.return_url
            }, None

        except Exception as e:
            await self._db_session.rollback()
            return None, f"创建任务失败 {e}"
    
    async def get_dialplan(self, threads_num) -> tuple[dict, str]:
        dialplan_list = self._dialplan_queue.get("dialplan", threads_num)
        dialplans = []
        for idx, item in enumerate(dialplan_list):
            try:
                if isinstance(item, str):
                    item = json.loads(item)
                dialplans.append({
                    "id": item["id"],
                    "phone": item["phone"],
                })
            except Exception as e:
                logger.error(f"解析 JSON 失败 {idx}: {e}, raw: {item}")
                continue
        if dialplans:
            return {"dialplans": dialplans}, None
        else:
            return None, "无有效拨号计划"

    async def update_dialplan_status(self, dialplan_id: int, _status: str):
        stmt = (
            update(Dialplan)
            .where(Dialplan.id == dialplan_id)
            .values(status = _status)
        )
        await self._db_session.execute(stmt)
        # stmt = (
        #     select(Dialplan)
        #     .where(Dialplan.phone == phone)
        # )
        # result = await self._db_session.execute(stmt)
        # dialplan = result.scalar_one_or_none()
        # if not dialplan:
        #     return
        # 检查 dialplan 所在的 task 是否已经都完成 dialplan.task_id
        # task_id = dialplan.task_id
        # stmt = (
        #     select(Dialplan)
        #     .where(Dialplan.task_id == task_id)
        #     .where(Dialplan.status == DialplanStatus.Free)
        # )
        # result = await self._db_session.execute(stmt)
        # # 

    async def update_task_status(self, dialplan_id: int):
        # 查找 dialplan_id 所在的 task id
        task_id = await self.get_task_id(dialplan_id)
        if not task_id:
            return
        # 检查所有 dialplan 中的所有 dialplan 中 task_id 的 status 是否都为 finish 
        result = await self._db_session.execute(
            select(Dialplan)
            .where(
                and_(
                    Dialplan.id == dialplan_id,
                    Dialplan.status != DialplanStatus.Finish
                )
            )
        )
        non_finish_dialplans = result.scalars().all()
        if not non_finish_dialplans:
            return
        # 更新 task 的 status 为 finish
        await self._db_session.execute(
            update(Task)
            .where(Task.id == task_id,)
            .values(status=DialplanStatus.Finish)
        )

    async def get_task_id(self, dialplan_id: int) -> int:
        result = await self._db_session.execute(
            select(Dialplan)
            .where(Dialplan.id == dialplan_id)
        )
        dialplan = result.scalar_one_or_none()
        if not dialplan:
            return None
        return dialplan.task_id


async def provide_dialplan_repository(db_session: AsyncSession) -> AsyncGenerator[DialplanRepository, None]:
    yield DialplanRepository(db_session)
