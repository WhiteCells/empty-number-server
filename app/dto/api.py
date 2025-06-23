from pydantic import BaseModel


class ApiGetDialplanQuery(BaseModel):
    threadsNum: int

class NotifyDto(BaseModel):
    threads_num: int
