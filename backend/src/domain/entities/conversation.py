"""Domain entity – a conversation thread."""
from dataclasses import dataclass, field

from src.domain.entities.message import Message


@dataclass
class Conversation:
    messages: list[Message] = field(default_factory=list)

    def add(self, message: Message) -> None:
        self.messages.append(message)

    def is_empty(self) -> bool:
        return len(self.messages) == 0
