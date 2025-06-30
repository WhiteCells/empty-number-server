from pydantic import BaseModel
from datetime import datetime
from app.dto.dialplan import GetDialplanResponseDto

class GetTasksQueryDto(BaseModel):
    page: int = 1
    size: int = 10

class GetTasksResponseDto(BaseModel):
    id: int
    status: str
    return_url: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class GetTaskResponseDto(BaseModel):
    id: int
    status: str
    return_url: str
    created_at: datetime
    updated_at: datetime
    dialplans: list[GetDialplanResponseDto] = []
    model_config = {
        "from_attributes": True
    }