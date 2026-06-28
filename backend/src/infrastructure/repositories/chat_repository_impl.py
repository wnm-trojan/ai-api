"""Infrastructure – domain repository implementations."""
from typing import AsyncIterator

from src.application.interfaces.ai_provider import IAIProvider
from src.application.interfaces.tool_executor import IToolExecutor
from src.domain.entities.chat import ChatResult, JsonResult, ToolCall
from src.domain.entities.message import Message
from src.domain.repositories.chat_repository import (
    IChatRepository,
    IJsonRepository,
    IStreamRepository,
    IToolRepository,
)


class ChatRepositoryImpl(IChatRepository):
    def __init__(self, provider: IAIProvider) -> None:
        self._provider = provider

    async def complete(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> ChatResult:
        return await self._provider.complete(messages, model, temperature, max_tokens)


class StreamRepositoryImpl(IStreamRepository):
    def __init__(self, provider: IAIProvider) -> None:
        self._provider = provider

    async def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
    ) -> AsyncIterator[str]:
        return await self._provider.stream(messages, model, temperature)


class JsonRepositoryImpl(IJsonRepository):
    def __init__(self, provider: IAIProvider) -> None:
        self._provider = provider

    async def complete_json(self, prompt: str, schema_hint: str) -> JsonResult:
        return await self._provider.complete_json(prompt, schema_hint)


class ToolRepositoryImpl(IToolRepository):
    def __init__(self, provider: IAIProvider, tool_executor: IToolExecutor) -> None:
        self._provider = provider
        self._tool_executor = tool_executor

    async def call_with_tools(self, user_message: str) -> ToolCall:
        return await self._provider.call_with_tools(user_message, self._tool_executor)
