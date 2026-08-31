"""
Base agent interface for EMMA.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from emma.perception.shared.input_event import InputEvent


class Agent(ABC):
    """Base class for all EMMA agents."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the agent's name."""
        raise NotImplementedError

    @abstractmethod
    async def run(self, event: InputEvent) -> str:
        """
        Process an input event and return a response.
        """
        raise NotImplementedError