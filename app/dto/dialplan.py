from pydantic import BaseModel
from datetime import datetime

class CreateDialplanDto(BaseModel):
    phone: list[str]
    return_url: str

class PutDialplanDto(BaseModel):
    phone: str

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
