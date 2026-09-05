from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class ModelProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def model(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> AsyncIterator[str]:
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        raise NotImplementedError