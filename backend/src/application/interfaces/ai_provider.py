"""Application interface – AI provider port."""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, AsyncIterator

from src.domain.entities.chat import ChatResult, JsonResult, ToolCall
from src.domain.entities.message import Message

if TYPE_CHECKING:
    from src.application.interfaces.tool_executor import IToolExecutor


class IAIProvider(ABC):
    @abstractmethod
    async def complete(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> ChatResult: ...

    @abstractmethod
    async def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
    ) -> AsyncIterator[str]: ...

    @abstractmethod
    async def complete_json(
        self,
        prompt: str,
        schema_hint: str,
    ) -> JsonResult: ...

    @abstractmethod
    async def call_with_tools(
        self,
        user_message: str,
        tool_executor: "IToolExecutor",
    ) -> ToolCall: ...
