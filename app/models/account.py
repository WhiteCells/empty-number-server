from sqlalchemy import String, Integer, DateTime, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import Mapped,  mapped_column, relationship
from datetime import datetime
from app.utils.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.client import Client

class AccountStatus:
    Free = "free"
    Used = "used"

class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="账户 ID")
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment="用户名")
    pwd: Mapped[str] = mapped_column(String(50), nullable=False, comment="密码")
    host: Mapped[str] = mapped_column(String(50), nullable=False, comment="主机地址")
    status: Mapped[str] = mapped_column(String(10), nullable=False, default=AccountStatus.Free, comment="状态")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="到期时间")

    # client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), nullable=True, comment="所属客户端 ID")
    # client: Mapped["Client"] = relationship("Client", back_populates="accounts")
