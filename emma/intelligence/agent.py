from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from emma.perception.shared.input_event import InputEvent


class Agent(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def run(self, event: InputEvent) -> str:
        raise NotImplementedError

    @abstractmethod
    async def stream(self, event: InputEvent) -> AsyncIterator[str]:
        raise NotImplementedError