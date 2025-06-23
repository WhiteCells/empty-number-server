from sqlalchemy import String, Integer, DateTime, Enum as SqlEnum
from sqlalchemy.orm import Mapped,  mapped_column, relationship
from datetime import datetime
from app.utils.database.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.account import Account

class ClientStatus:
    Online = "online"
    Offline = "offline"

"""
每个客户端有多个账号
"""
class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="客户端 ID")
    uuid: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, comment="客户端 UUID")
    status: Mapped[str] = mapped_column(String(10), nullable=False, default=ClientStatus.Offline, comment="状态")
    threads_num: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="线程数")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    accounts: Mapped[List["Account"]] = relationship("Account", back_populates="client")
