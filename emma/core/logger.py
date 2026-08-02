"""
EMMA Logging System

Provides a centralized logging system for EMMA.

Author: Varun Patil
"""

import logging
from pathlib import Path

# Ensure the logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "emma.log"

# Common log format
LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger for a module.

    Example:
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)