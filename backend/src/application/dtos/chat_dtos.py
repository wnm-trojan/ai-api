"""Application DTOs – internal data transfer objects."""
from typing import Any
from pydantic import BaseModel, Field


class MessageDTO(BaseModel):
    role: str
    content: str


class ChatInputDTO(BaseModel):
    messages: list[MessageDTO]
    model: str = "gpt-4o-mini"
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=1000, ge=1, le=4096)


class StreamInputDTO(BaseModel):
    messages: list[MessageDTO]
    model: str = "gpt-4o-mini"
    temperature: float = Field(default=0.7, ge=0, le=2)


class JsonInputDTO(BaseModel):
    prompt: str
    schema_hint: str = ""


class ToolCallInputDTO(BaseModel):
    user_message: str
