"""
EMMA Application

Controls the lifecycle of EMMA.
"""

from emma.core.config import settings
from emma.core.logger import get_logger

logger = get_logger(__name__)


class Application:
    """
    Main application controller.
    """

    def __init__(self):
        self.name = settings.app.name
        self.version = settings.app.version

    def start(self):
        logger.info(f"Starting {self.name} v{self.version}")
        logger.info("Application started successfully.")

    def stop(self):
        logger.info("Shutting down EMMA...")
        logger.info("Application stopped.")