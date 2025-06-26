import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, or_
from app.models.dialplan import Dialplan, DialplanStatus
from app.utils.dialplan_queue import get_dialplan_queue
from app.utils.database.session import async_session
from app.utils.logger import logger

_que = get_dialplan_queue()


# 定时任务
async def fetch_free_dialplans_to_queue():
    while True:
        # logger.info("fetching free dialplans...")
        timeout_time = datetime.now() - timedelta(seconds=120)

        async with async_session() as db_session:
            async with db_session.begin():
                # 状态为处理中或者超时
                result = await db_session.execute(
                    select(Dialplan)
                    .where(
                        or_(
                            Dialplan.status == DialplanStatus.Processing,
                            Dialplan.status == DialplanStatus.Free
                        )
                    )
                    .where(Dialplan.updated_at < timeout_time)
                    .limit(_que.maxsize)
                    .with_for_update()
                )
                timeout_dialplans = result.scalars().all()
                for dialplan in timeout_dialplans:
                    if _que.size("dialplan") < _que.maxsize:
                        _que.put("dialplan", dialplan.phone)
                        dialplan.updated_at = datetime.now()
                        dialplan.status = DialplanStatus.Queued
                        logger.info(f"push timeout dialplan: {dialplan.phone}")

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
