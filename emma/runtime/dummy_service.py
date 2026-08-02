"""
Dummy service used to validate EMMA's runtime architecture.
"""

from emma.core.logger import get_logger
from emma.runtime.base_service import BaseService

logger = get_logger(__name__)


class DummyService(BaseService):
    """A simple service for testing the runtime."""

    async def initialize(self) -> None:
        logger.info("DummyService initialized.")

    async def start(self) -> None:
        logger.info("DummyService started.")

    async def stop(self) -> None:
        logger.info("DummyService stopped.")