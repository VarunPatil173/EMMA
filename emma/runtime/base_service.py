"""
Base Service

Defines the lifecycle contract for every long-running
service in EMMA.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from emma.runtime.service_state import ServiceState


class BaseService(ABC):
    """
    Base class for all EMMA services.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
    ) -> None:

        self.name = name
        self.description = description
        self.state = ServiceState.CREATED

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the service."""

    @abstractmethod
    async def start(self) -> None:
        """Start the service."""

    @abstractmethod
    async def stop(self) -> None:
        """Stop the service."""