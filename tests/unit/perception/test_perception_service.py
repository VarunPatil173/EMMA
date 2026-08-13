import pytest

from emma.perception.perception_service import PerceptionService
from emma.perception.audio.worker import PerceptionWorker


class FakeWorker:
    def __init__(self):
        self.engine = FakeEngine()
        self.started = False
        self.stopped = False

    async def start(self):
        self.started = True

    async def stop(self):
        self.stopped = True


class FakeEngine:
    def __init__(self):
        self._running = False

    async def start(self):
        self._running = True

    async def stop(self):
        self._running = False


@pytest.mark.anyio
async def test_perception_service_lifecycle():
    worker = FakeWorker()
    service = PerceptionService(worker)

    assert service.name == "perception"
    assert service.state.value == "CREATED"

    await service.initialize()
    await service.start()

    assert worker.started is True
    assert service.engine._running is True

    await service.stop()

    assert worker.stopped is True
    assert service.engine._running is False