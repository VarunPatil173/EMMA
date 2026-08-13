"""
EMMA Perception Service.

Integrates the Perception Engine with EMMA's runtime
service lifecycle.
"""

from __future__ import annotations

from emma.core.logger import get_logger
from emma.perception.audio.worker import PerceptionWorker
from emma.perception.engine import PerceptionEngine
from emma.runtime.base_service import BaseService

logger = get_logger(__name__)


class PerceptionService(BaseService):
    """Runtime service responsible for EMMA perception."""

    def __init__(
        self,
        worker: PerceptionWorker,
    ) -> None:
        super().__init__(
            name="perception",
            description="EMMA multimodal perception service",
        )

        self.engine = worker.engine
        self.worker = worker

    async def initialize(self) -> None:
        """Initialize the perception subsystem."""

        logger.info("Initializing Perception Service.")

    async def start(self) -> None:
        """Start the perception engine and worker."""

        await self.engine.start()
        await self.worker.start()

        logger.info("Perception Service started.")

    async def stop(self) -> None:
        """Stop the perception worker and engine."""

        await self.worker.stop()
        await self.engine.stop()

        logger.info("Perception Service stopped.")