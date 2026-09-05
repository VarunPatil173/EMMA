import pytest

from emma.intelligence.agent import Agent
from emma.interface.text_interface import TextInterface
from emma.perception.engine import PerceptionEngine


class FakeAgent(Agent):
    @property
    def name(self) -> str:
        return "fake"

    async def run(self, event) -> str:
        return f"AI response to: {event.text}"

    async def stream(self, event):
        yield f"AI response to: {event.text}"


@pytest.mark.asyncio
async def test_text_interface_has_agent():
    engine = PerceptionEngine()
    agent = FakeAgent()

    interface = TextInterface(engine, agent)

    assert interface.engine is engine
    assert interface.agent is agent