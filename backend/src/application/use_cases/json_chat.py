"""Application use case – structured JSON chat."""
from src.domain.entities.chat import JsonResult
from src.domain.repositories.chat_repository import IJsonRepository


class JsonChatUseCase:
    def __init__(self, repo: IJsonRepository) -> None:
        self._repo = repo

    async def execute(self, prompt: str, schema_hint: str) -> JsonResult:
        if not prompt.strip():
            raise ValueError("prompt cannot be blank")
        return await self._repo.complete_json(prompt, schema_hint)
