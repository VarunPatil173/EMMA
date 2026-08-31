"""
Model provider abstraction for EMMA.

All language-model providers must implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class ModelProvider(ABC):
    """Abstract interface for every LLM used by EMMA."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def model(self) -> str:
        """Return the model identifier."""
        raise NotImplementedError

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """
        Generate a complete response.

        This is useful when the caller needs the entire response at once.
        """
        raise NotImplementedError

    @abstractmethod
    async def stream(self, prompt: str) -> AsyncIterator[str]:
        """
        Stream a response token/chunk by token/chunk.

        Providers should yield text as soon as it becomes available.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """Return True when the provider is currently usable."""
        raise NotImplementedError