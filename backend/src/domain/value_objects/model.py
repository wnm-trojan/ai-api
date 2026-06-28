"""Domain value object – AI model identifier."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Model:
    name: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("model name cannot be blank")

    @classmethod
    def default(cls) -> "Model":
        return cls(name="gpt-4o-mini")
