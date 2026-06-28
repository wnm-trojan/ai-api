"""Domain repository interfaces (ports)."""
from abc import ABC, abstractmethod
from typing import AsyncIterator

from src.domain.entities.chat import ChatResult, JsonResult, ToolCall
from src.domain.entities.message import Message


class IChatRepository(ABC):
    @abstractmethod
    async def complete(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> ChatResult: ...


class IStreamRepository(ABC):
    @abstractmethod
    async def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
    ) -> AsyncIterator[str]: ...


class IJsonRepository(ABC):
    @abstractmethod
    async def complete_json(
        self,
        prompt: str,
        schema_hint: str,
    ) -> JsonResult: ...


class IToolRepository(ABC):
    @abstractmethod
    async def call_with_tools(
        self,
        user_message: str,
    ) -> ToolCall: ...
