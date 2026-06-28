"""Application interface – tool executor port."""
from abc import ABC, abstractmethod
from typing import Any


class IToolExecutor(ABC):
    @abstractmethod
    def execute(self, name: str, args: dict) -> Any: ...
