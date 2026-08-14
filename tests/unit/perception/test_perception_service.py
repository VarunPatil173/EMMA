import pytest

from emma.perception.engine import PerceptionEngine
from emma.perception.perception_service import PerceptionService


class FakeWorker:
    """Fake perception worker for service tests."""

    def __init__(self) -> None:
        self.started = False
        self.stopped = False

    async def start(self) -> None:
        self.started = True

    async def stop(self) -> None:
        self.stopped = True


@pytest.mark.anyio
async def test_perception_service_lifecycle():
    engine = PerceptionEngine()
    worker = FakeWorker()

    service = PerceptionService(
        engine=engine,
        worker=worker,
    )

    assert service.name == "perception"
    assert service.state.value == "CREATED"

    await service.initialize()
    await service.start()

    assert worker.started is True
    assert service.engine._running is True

    await service.stop()

    assert worker.stopped is True
    assert service.engine._running is False