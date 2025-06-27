import asyncio
import json
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, or_, and_
from app.models.dialplan import Dialplan, DialplanStatus
from app.utils.dialplan_queue import get_dialplan_queue
from app.utils.database.session import async_session
from app.utils.logger import logger

_que = get_dialplan_queue()


# 定时任务
async def fetch_timeout_dialplans_to_queue():
    while True:
        # logger.info("fetching timeout dialplans...")
        timeout_time = datetime.now() - timedelta(seconds=150)

        async with async_session() as db_session:
            async with db_session.begin():
                result = await db_session.execute(
                    select(Dialplan)
                    .where(
                        and_(
                            Dialplan.status == DialplanStatus.Processing,
                            Dialplan.updated_at < timeout_time,
                        )
                    )
                    .limit(_que.maxsize)
                    .with_for_update()
                )
                timeout_dialplans = result.scalars().all()
                for dialplan in timeout_dialplans:
                    if _que.size("dialplan") < _que.maxsize:
                        # 存储的时候存 json {"id": "", "phone": dialplan.phone}
                        payload = json.dumps({"id": dialplan.id, "phone": dialplan.phone})
                        _que.put("dialplan", payload)
                        dialplan.updated_at = datetime.now()
                        dialplan.status = DialplanStatus.Queued
                        logger.info(f"push timeout dialplan: {dialplan.phone}")

        await asyncio.sleep(3)


async def fetch_free_dialplans_to_queue():
    while True:
        # logger.info("fetching free dialplans...")

        async with async_session() as db_session:
            async with db_session.begin():
                result = await db_session.execute(
                    select(Dialplan)
                    .where(
                        and_(
                            Dialplan.status == DialplanStatus.Free,
                        )
                    )
                    .limit(_que.maxsize)
                    .with_for_update()
                )
                timeout_dialplans = result.scalars().all()
                for dialplan in timeout_dialplans:
                    if _que.size("dialplan") < _que.maxsize:
                        # 存储的时候存 json {"id": "", "phone": dialplan.phone}
                        payload = json.dumps({"id": dialplan.id, "phone": dialplan.phone})
                        _que.put("dialplan", payload)
                        dialplan.updated_at = datetime.now()
                        dialplan.status = DialplanStatus.Queued
                        logger.info(f"push free dialplan: {dialplan.phone}")

        await asyncio.sleep(3)


async def fetch_queued_to_queue():
    async with async_session() as db_session:
        async with db_session.begin():
            result = await db_session.execute(
                select(Dialplan)
                .where(Dialplan.status == DialplanStatus.Queued)
            )
            dialplans = result.scalars().all()
            for dialplan in dialplans:
                _que.put("dialplan", dialplan.phone)
                logger.info(f"push queued dialplan: {dialplan.phone}")
