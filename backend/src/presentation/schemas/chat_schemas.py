"""Presentation schemas – API request/response models."""
from typing import Any
from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    role: str = Field(..., examples=["user"])
    content: str = Field(..., examples=["Hello!"])


class ChatRequestSchema(BaseModel):
    messages: list[MessageSchema]
    model: str = "gpt-4o-mini"
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=1000, ge=1, le=4096)


class StreamRequestSchema(BaseModel):
    messages: list[MessageSchema]
    model: str = "gpt-4o-mini"
    temperature: float = Field(default=0.7, ge=0, le=2)


class JsonRequestSchema(BaseModel):
    prompt: str = Field(..., examples=["Extract name and age from: 'Alice is 30'"])
    schema_hint: str = Field(default="", examples=['{"name": "string", "age": "number"}'])


class ToolCallRequestSchema(BaseModel):
    user_message: str = Field(..., examples=["What is the weather in Tokyo?"])


class TokenUsageSchema(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponseSchema(BaseModel):
    message: str
    model: str
    usage: TokenUsageSchema
    latency_ms: int


class JsonResponseSchema(BaseModel):
    data: dict[str, Any]


class ToolCallResponseSchema(BaseModel):
    tool_called: str
    tool_args: dict[str, Any]
    tool_result: Any
    final_answer: str


class HealthResponseSchema(BaseModel):
    status: str
    version: str
    openai_configured: bool
