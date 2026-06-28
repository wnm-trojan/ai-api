"""Application mappers – DTO ↔ domain entity conversions."""
from src.application.dtos.chat_dtos import MessageDTO
from src.domain.entities.message import Message


def to_message(dto: MessageDTO) -> Message:
    return Message(role=dto.role, content=dto.content)


def to_messages(dtos: list[MessageDTO]) -> list[Message]:
    return [to_message(d) for d in dtos]
