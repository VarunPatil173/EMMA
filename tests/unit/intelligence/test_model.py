from collections.abc import AsyncIterator

import pytest

from emma.intelligence.model import ModelProvider


class FakeModel(ModelProvider):
    """Test implementation of ModelProvider."""

    @property
    def name(self) -> str:
        return "fake"

    @property
    def model(self) -> str:
        return "fake-model"

    async def generate(self, prompt: str) -> str:
        return f"Response: {prompt}"

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        yield "Response: "
        yield prompt

    async def health_check(self) -> bool:
        return True


def test_model_provider_metadata():
    model = FakeModel()

    assert model.name == "fake"
    assert model.model == "fake-model"


@pytest.mark.asyncio
async def test_model_provider_generate():
    model = FakeModel()

    response = await model.generate("Hello")

    assert response == "Response: Hello"


@pytest.mark.asyncio
async def test_model_provider_stream():
    model = FakeModel()

    chunks = [chunk async for chunk in model.stream("Hello")]

    assert chunks == ["Response: ", "Hello"]


@pytest.mark.asyncio
async def test_model_provider_health_check():
    model = FakeModel()

    assert await model.health_check() is True