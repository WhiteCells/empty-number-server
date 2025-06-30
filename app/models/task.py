from app.utils.database.base import Base
from sqlalchemy import Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.dialplan import Dialplan

class TaskStatus:
    Pending = "pending"
    Processing = "processing"
    Completed = "completed"

"""
一个任务包含多个电话号码
"""
class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="任务 ID")
    status: Mapped[str] = mapped_column(String(20), default=TaskStatus.Pending, comment="任务状态")
    return_url: Mapped[str] = mapped_column(String(255), nullable=False, comment="回调地址")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    dialplans: Mapped[list["Dialplan"]] = relationship("Dialplan", back_populates="task", cascade="all, delete-orphan")