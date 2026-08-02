"""
EMMA Service Registry

Stores and provides access to all registered services.
"""

from __future__ import annotations

from typing import Dict

from emma.runtime.base_service import BaseService


class ServiceRegistry:
    """
    Central registry for all EMMA services.
    """

    def __init__(self) -> None:
        self._services: Dict[str, BaseService] = {}

    def register(self, name: str, service: BaseService) -> None:
        """
        Register a service.
        """
        if name in self._services:
            raise ValueError(f"Service '{name}' is already registered.")

        self._services[name] = service

    def get(self, name: str) -> BaseService:
        """
        Retrieve a service by name.
        """
        if name not in self._services:
            raise KeyError(f"Service '{name}' is not registered.")

        return self._services[name]

    def exists(self, name: str) -> bool:
        """
        Check whether a service exists.
        """
        return name in self._services

    def all(self) -> list[BaseService]:
        """
        Return all registered services.
        """
        return list(self._services.values())