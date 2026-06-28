"""Domain entity – chat completion results."""
from dataclasses import dataclass
from typing import Any

from src.domain.entities.message import TokenUsage


@dataclass(frozen=True)
class ChatResult:
    content: str
    model: str
    usage: TokenUsage
    latency_ms: int


@dataclass(frozen=True)
class JsonResult:
    data: dict[str, Any]


@dataclass(frozen=True)
class ToolCall:
    tool_name: str
    tool_args: dict[str, Any]
    tool_result: Any
    final_answer: str
