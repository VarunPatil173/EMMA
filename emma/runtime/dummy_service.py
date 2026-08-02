"""
Dummy service used to validate EMMA's runtime architecture.
"""

from emma.core.logger import get_logger
from emma.runtime.base_service import BaseService
from emma.runtime.service_state import ServiceState

logger = get_logger(__name__)


class DummyService(BaseService):

    def __init__(self):
        super().__init__(
            name="Dummy Service",
            description="Runtime validation service."
        )

    async def initialize(self):
        self.state = ServiceState.INITIALIZED
        logger.info(f"{self.name} initialized.")

    async def start(self):
        self.state = ServiceState.RUNNING
        logger.info(f"{self.name} started.")

    async def stop(self):
        self.state = ServiceState.STOPPED
        logger.info(f"{self.name} stopped.")