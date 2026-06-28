"""Infrastructure – Anthropic provider (stub for future implementation)."""
from typing import AsyncIterator

from src.application.interfaces.ai_provider import IAIProvider
from src.application.interfaces.tool_executor import IToolExecutor
from src.domain.entities.chat import ChatResult, JsonResult, ToolCall
from src.domain.entities.message import Message
from src.domain.exceptions import AIProviderError


class AnthropicProvider(IAIProvider):
    """Placeholder – wire anthropic SDK here when needed."""

    async def complete(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> ChatResult:
        raise AIProviderError("Anthropic provider not yet implemented")

    async def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
    ) -> AsyncIterator[str]:
        raise AIProviderError("Anthropic provider not yet implemented")

    async def complete_json(self, prompt: str, schema_hint: str) -> JsonResult:
        raise AIProviderError("Anthropic provider not yet implemented")

    async def call_with_tools(
        self,
        user_message: str,
        tool_executor: IToolExecutor,
    ) -> ToolCall:
        raise AIProviderError("Anthropic provider not yet implemented")
