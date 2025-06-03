from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class GetUserDTO(BaseModel):
    id: int
    username: str
    email: EmailStr
