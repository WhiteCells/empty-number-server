from pydantic import BaseModel
from datetime import datetime

class CreateDialplanDto(BaseModel):
    phone: list[str]
    return_url: str

class PutDialplanDto(BaseModel):
    dialplan_id: int
    account_id: int
    phone: str
    status: str

class DialplanStatusDto(BaseModel):
    id: int
    phone: str
    status: str
    account_id: int

class CreateDialplanResponseDto(BaseModel):
    id: int
    phone: str
    client_id: str | None = None
    status: str
    result: str | None = None
    created_at: datetime
    updated_at: datetime
    task_id: int
    model_config = {
        "from_attributes": True
    }

class GetDialplanResponseDto(BaseModel):
    id: int
    phone: str
    client_id: str | None = None
    status: str
    result: str | None = None
    created_at: datetime
    updated_at: datetime
    task_id: int
    model_config = {
        "from_attributes": True
    }