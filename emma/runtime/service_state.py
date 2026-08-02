"""
Service states used by EMMA services.
"""

from enum import Enum


class ServiceState(str, Enum):
    """
    Represents the lifecycle state of a service.
    """

    CREATED = "CREATED"
    INITIALIZED = "INITIALIZED"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"