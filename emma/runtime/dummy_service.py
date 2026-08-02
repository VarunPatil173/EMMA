"""
Dummy service used to validate EMMA's runtime architecture.
"""

from emma.core.logger import get_logger
from emma.runtime.base_service import BaseService
from emma.runtime.service_state import ServiceState

logger = get_logger(__name__)


class DummyService(BaseService):
    """A simple service for testing the runtime."""

    async def initialize(self):
        self.state = ServiceState.INITIALIZED
        logger.info("DummyService initialized.")

    async def start(self):
        self.state = ServiceState.RUNNING
        logger.info("DummyService started.")

    async def stop(self):
        self.state = ServiceState.STOPPED
        logger.info("DummyService stopped.")