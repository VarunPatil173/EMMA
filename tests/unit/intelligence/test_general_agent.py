import pytest

from emma.intelligence.general_agent import GeneralAgent
from emma.intelligence.model import ModelProvider
from emma.perception.shared.input_event import InputEvent


class FakeModel(ModelProvider):
    @property
    def name(self) -> str:
        return "fake"

    @property
    def model(self) -> str:
        return "fake-model"

    async def generate(self, prompt: str) -> str:
        return f"AI response to: {prompt}"

    async def stream(self, prompt: str):
        yield f"AI response to: {prompt}"

    async def health_check(self) -> bool:
        return True


@pytest.mark.asyncio
async def test_general_agent_responds_to_text():
    agent = GeneralAgent(FakeModel())

    event = InputEvent(
        source="text",
        text="Hello EMMA",
    )

    response = await agent.run(event)

    assert response == "AI response to: Hello EMMA"