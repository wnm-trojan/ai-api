"""Domain entity – chat message and token usage."""
from dataclasses import dataclass

from src.domain.value_objects.role import Role


@dataclass(frozen=True)
class Message:
    role: str
    content: str

    def __post_init__(self) -> None:
        valid = {r.value for r in Role}
        if self.role not in valid:
            raise ValueError(f"invalid role: {self.role}")


@dataclass(frozen=True)
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
