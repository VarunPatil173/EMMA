from abc import ABC, abstractmethod

from emma.runtime.service_state import ServiceState


class BaseService(ABC):

    def __init__(self) -> None:
        self.state = ServiceState.CREATED

    @abstractmethod
    async def initialize(self) -> None:
        ...

    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def stop(self) -> None:
        ...