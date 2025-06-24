from pydantic import BaseModel


class CreateClientDto(BaseModel):
    name: str
    uuid: str

class PutClientDto(BaseModel):
    name: str
    uuid: str

class GetClientByUuidDto(BaseModel):
    id: int
    uuid: str

class GetClientQueryDto(BaseModel):
    pass