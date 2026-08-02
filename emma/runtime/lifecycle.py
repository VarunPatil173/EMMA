"""
EMMA Lifecycle Manager

Coordinates the lifecycle of all registered services.
"""

from __future__ import annotations

from emma.core.logger import get_logger
from emma.runtime.service_registry import ServiceRegistry
from emma.runtime.service_state import ServiceState

logger = get_logger(__name__)


class LifecycleManager:
    """
    Controls initialization, startup, and shutdown
    of every registered service.
    """

    def __init__(self, registry: ServiceRegistry) -> None:
        self._registry = registry

    async def initialize(self) -> None:
        logger.info("Initializing services...")

        for service in self._registry.all():
            try:
                await service.initialize()

            except Exception:
                service.state = ServiceState.FAILED
                logger.exception(
                    f"{service.__class__.__name__} failed during initialization."
                )
                raise

        logger.info("All services initialized.")

    async def start(self) -> None:
        logger.info("Starting services...")

        started_services = []

        try:
            for service in self._registry.all():
                await service.start()
                started_services.append(service)

        except Exception:
            service.state = ServiceState.FAILED

            logger.exception(
                f"{service.__class__.__name__} failed during startup."
            )

            logger.info("Stopping already-started services...")

            for started in reversed(started_services):
                try:
                    await started.stop()
                except Exception:
                    logger.exception(
                        f"Failed to stop {started.__class__.__name__}"
                    )

            raise

        logger.info("All services started.")

    async def stop(self) -> None:
        logger.info("Stopping services...")

        for service in reversed(self._registry.all()):
            try:
                await service.stop()

            except Exception:
                logger.exception(
                    f"Failed to stop {service.__class__.__name__}"
                )

        logger.info("All services stopped.")