from pydantic import BaseModel
from datetime import datetime


class CreateClientDto(BaseModel):
    name: str
    uuid: str

class PutClientDto(BaseModel):
    name: str
    uuid: str

class GetClientByUuidDto(BaseModel):
    id: int
    uuid: str

class GetClientsQueryDto(BaseModel):
    page: int
    size: int

class GetClientDto(BaseModel):
    id: int
    uuid: str
    status: str
    threads_num: int
    created_at: datetime
    updated_at: datetime
    model_config = {
        "from_attributes": True
    }