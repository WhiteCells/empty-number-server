from pydantic import BaseModel
from datetime import datetime


class Account(BaseModel):
    host: str
    name: str
    pwd: str

class CreateAccountDto(BaseModel):
    account: list[Account]

class PutAccountDto(BaseModel):
    host: str = None
    name: str = None
    pwd: str = None

class CreateAccountResponseDto(BaseModel):
    host: str = None
    name: str = None
    pwd: str = None
    model_config = {
        "from_attributes": True
    }

class GetAccountResponseDto(BaseModel):
    id: int
    name: str
    pwd: str
    host: str
    status: str
    created_at: datetime
    updated_at: datetime
    expired_at: datetime
    model_config = {
        "from_attributes": True
    }
