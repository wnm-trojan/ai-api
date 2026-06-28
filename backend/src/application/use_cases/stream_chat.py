"""Application use case – streaming chat."""
from typing import AsyncIterator

from src.domain.entities.message import Message
from src.domain.repositories.chat_repository import IStreamRepository


class StreamChatUseCase:
    def __init__(self, repo: IStreamRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
    ) -> AsyncIterator[str]:
        if not messages:
            raise ValueError("messages cannot be empty")
        return await self._repo.stream(messages, model, temperature)
