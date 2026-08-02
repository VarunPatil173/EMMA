"""
EMMA Lifecycle Manager

Coordinates the lifecycle of all registered services.
"""

from __future__ import annotations

import time

from emma.core.logger import get_logger
from emma.runtime.base_service import BaseService
from emma.runtime.service_registry import ServiceRegistry
from emma.runtime.service_state import ServiceState

logger = get_logger(__name__)


class LifecycleManager:
    """
    Coordinates the lifecycle of all registered services.

    Responsibilities:
    - Initialize services
    - Start services
    - Stop services
    - Handle startup failures
    - Measure startup performance
    """

    def __init__(self, registry: ServiceRegistry) -> None:
        self._registry = registry

    async def initialize(self) -> None:
        """
        Initialize every registered service.
        """

        logger.info("Initializing services...")

        total_start = time.perf_counter()

        for service in self._registry.all():

            service_start = time.perf_counter()

            try:
                await service.initialize()

                elapsed = (time.perf_counter() - service_start) * 1000

                logger.info(
                    f"{service.name:<25} initialized in {elapsed:.2f} ms"
                )

            except Exception:
                service.state = ServiceState.FAILED

                logger.exception(
                    f"{service.name} failed during initialization."
                )

                raise

        total_elapsed = (time.perf_counter() - total_start) * 1000

        logger.info(
            f"Initialization completed in {total_elapsed:.2f} ms"
        )

    async def start(self) -> None:
        """
        Start every registered service.
        """

        logger.info("Starting services...")

        total_start = time.perf_counter()
        started_services: list[BaseService] = []

        try:
            for service in self._registry.all():

                service_start = time.perf_counter()

                await service.start()

                elapsed = (time.perf_counter() - service_start) * 1000

                logger.info(
                    f"{service.name:<25} started in {elapsed:.2f} ms"
                )

                started_services.append(service)

        except Exception:
            service.state = ServiceState.FAILED

            logger.exception(
                f"{service.name} failed during startup."
            )

            logger.info("Stopping already-started services...")

            for started_service in reversed(started_services):
                try:
                    await started_service.stop()
                except Exception:
                    logger.exception(
                        f"Failed to stop {started_service.name}"
                    )

            raise

        total_elapsed = (time.perf_counter() - total_start) * 1000

        logger.info(
            f"Startup completed in {total_elapsed:.2f} ms"
        )

        logger.info("All services started.")

    async def stop(self) -> None:
        """
        Stop every registered service in reverse order.
        """

        logger.info("Stopping services...")

        for service in reversed(self._registry.all()):

            try:
                await service.stop()

            except Exception:
                service.state = ServiceState.FAILED

                logger.exception(
                    f"Failed to stop {service.name}"
                )

        logger.info("All services stopped.")