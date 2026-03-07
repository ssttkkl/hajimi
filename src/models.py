from pydantic import BaseModel
from typing import Literal

class A2APart(BaseModel):
    text: str | None = None
    file: str | None = None

class A2AMessage(BaseModel):
    role: Literal["user", "agent"]
    parts: list[A2APart]

class A2ATask(BaseModel):
    id: str = ""  # 空字符串表示单轮对话
    messages: list[A2AMessage]

class SessionData(BaseModel):
    id: str
    metadata: list[str | None]
    messages: list[A2AMessage]
    created_at: str
    updated_at: str
