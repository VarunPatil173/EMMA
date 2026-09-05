from collections.abc import AsyncIterator

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

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        return f"FAKE RESPONSE: {prompt}"

    async def stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> AsyncIterator[str]:
        yield "FAKE "
        yield "STREAM"

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

    assert response == "FAKE RESPONSE: Hello EMMA"


@pytest.mark.asyncio
async def test_general_agent_streams_text():
    agent = GeneralAgent(FakeModel())

    event = InputEvent(
        source="text",
        text="Hello EMMA",
    )

    chunks = []

    async for chunk in agent.stream(event):
        chunks.append(chunk)

    assert "".join(chunks) == "FAKE STREAM"


@pytest.mark.asyncio
async def test_general_agent_rejects_empty_text():
    agent = GeneralAgent(FakeModel())

    event = InputEvent(
        source="text",
        text="",
    )

    response = await agent.run(event)

    assert response == "I didn't receive any text."