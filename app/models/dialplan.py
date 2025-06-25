from sqlalchemy import String, Integer, DateTime, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import Mapped,  mapped_column, relationship
from datetime import datetime
from app.utils.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task

class DialplanStatus:
    Free = "free"
    Processing = "processing"
    Finish = "finish"

class DialplanResult:
    Empty = "empty"        # 空号
    Shutdown = "shutdown"  # 关机
    Suspend = "suspend"    # 停机
    Busy = "busy"          # 占线

class Dialplan(Base):
    __tablename__ = "dialplan"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="拨号 ID")
    phone: Mapped[str] = mapped_column(String(64), nullable=False, comment="手机号码")
    client_id: Mapped[str] = mapped_column(String(64), nullable=True, comment="客户端 ID")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=DialplanStatus.Free, comment="状态")
    result: Mapped[str] = mapped_column(String(20), nullable=True, comment="空号识别结果")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    expired_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="过期时间")

    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    task: Mapped["Task"] = relationship("Task", back_populates="dialplans")
