"""Application use case – chat completion."""
from src.domain.entities.chat import ChatResult
from src.domain.entities.message import Message
from src.domain.repositories.chat_repository import IChatRepository


class ChatCompletionUseCase:
    def __init__(self, repo: IChatRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> ChatResult:
        if not messages:
            raise ValueError("messages cannot be empty")
        return await self._repo.complete(messages, model, temperature, max_tokens)
