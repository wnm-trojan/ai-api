"""Application use case – function / tool calling."""
from src.domain.entities.chat import ToolCall
from src.domain.repositories.chat_repository import IToolRepository


class FunctionCallUseCase:
    def __init__(self, repo: IToolRepository) -> None:
        self._repo = repo

    async def execute(self, user_message: str) -> ToolCall:
        if not user_message.strip():
            raise ValueError("user_message cannot be blank")
        return await self._repo.call_with_tools(user_message)
