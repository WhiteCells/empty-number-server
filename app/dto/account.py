from pydantic import BaseModel


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