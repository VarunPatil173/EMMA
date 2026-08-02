"""
EMMA Application

Coordinates the startup and shutdown of EMMA.

Author: Varun Patil
"""

from __future__ import annotations

from emma.core.config import settings
from emma.core.logger import get_logger
from emma.runtime.base_service import BaseService
from emma.runtime.lifecycle import LifecycleManager
from emma.runtime.service_registry import ServiceRegistry

logger = get_logger(__name__)


class Application:
    """
    Main application controller.

    Responsibilities:
    - Own the Service Registry
    - Own the Lifecycle Manager
    - Start EMMA
    - Stop EMMA
    """

    def __init__(self) -> None:
        self.name = settings.app.name
        self.version = settings.app.version

        self.registry = ServiceRegistry()
        self.lifecycle = LifecycleManager(self.registry)

    def register_service(self, name: str, service: BaseService) -> None:
        """
        Register a service with the application.

        Args:
            name: Unique service name.
            service: Service instance.
        """
        logger.info(f"Registering service: {name}")
        self.registry.register(name, service)

    async def start(self) -> None:
        """
        Start EMMA.
        """
        logger.info("=" * 50)
        logger.info(f"Starting {self.name} v{self.version}")

        await self.lifecycle.initialize()
        await self.lifecycle.start()

        logger.info("EMMA is ready.")
        logger.info("=" * 50)

    async def stop(self) -> None:
        """
        Stop EMMA.
        """
        logger.info("=" * 50)
        logger.info("Shutting down EMMA...")

        await self.lifecycle.stop()

        logger.info("EMMA shutdown complete.")
        logger.info("=" * 50)