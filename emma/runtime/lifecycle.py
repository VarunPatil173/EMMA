"""
EMMA Lifecycle Manager

Coordinates the lifecycle of all registered services.
"""

from __future__ import annotations

from emma.core.logger import get_logger
from emma.runtime.service_registry import ServiceRegistry

logger = get_logger(__name__)


class LifecycleManager:
    """
    Controls initialization, startup, and shutdown
    of every registered service.
    """

    def __init__(self, registry: ServiceRegistry) -> None:
        self._registry = registry

    async def initialize(self) -> None:
        """
        Initialize every registered service.
        """
        logger.info("Initializing services...")

        for service in self._registry.all():
            await service.initialize()

        logger.info("All services initialized.")

    async def start(self) -> None:
        """
        Start every registered service.
        """
        logger.info("Starting services...")

        for service in self._registry.all():
            await service.start()

        logger.info("All services started.")

    async def stop(self) -> None:
        """
        Stop every registered service.
        """

        logger.info("Stopping services...")

        # Reverse order is safer
        for service in reversed(self._registry.all()):
            await service.stop()

        logger.info("All services stopped.")