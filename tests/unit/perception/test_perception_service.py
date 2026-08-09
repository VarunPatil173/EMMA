import pytest

from emma.perception.perception_service import PerceptionService


@pytest.mark.anyio
async def test_perception_service_lifecycle():
    service = PerceptionService()

    assert service.name == "perception"
    assert service.state.value == "CREATED"

    await service.initialize()
    await service.start()

    assert service.engine._running is True

    await service.stop()

    assert service.engine._running is False