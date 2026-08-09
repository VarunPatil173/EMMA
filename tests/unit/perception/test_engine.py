import pytest

from emma.perception.engine import PerceptionEngine
from emma.perception.input.text_input import TextInput


@pytest.mark.anyio
async def test_perception_engine_processes_event():
    engine = PerceptionEngine()

    await engine.start()

    event = TextInput().create_event("Open YouTube")

    result = await engine.process(event)

    assert result is event
    assert result.source == "text"
    assert result.text == "Open YouTube"

    await engine.stop()


@pytest.mark.anyio
async def test_perception_engine_requires_start():
    engine = PerceptionEngine()

    event = TextInput().create_event("Open YouTube")

    with pytest.raises(RuntimeError):
        await engine.process(event)