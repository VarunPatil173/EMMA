import pytest

from emma.intelligence.model import ModelProvider
from emma.intelligence.model_router import ModelRouter


class FakeProvider(ModelProvider):
    def __init__(
        self,
        provider_name: str,
        model_name: str,
        healthy: bool,
    ) -> None:
        self._provider_name = provider_name
        self._model_name = model_name
        self._healthy = healthy

    @property
    def name(self) -> str:
        return self._provider_name

    @property
    def model(self) -> str:
        return self._model_name

    async def generate(self, prompt: str) -> str:
        return f"{self._provider_name}: {prompt}"

    async def stream(self, prompt: str):
        yield f"{self._provider_name}: "
        yield prompt

    async def health_check(self) -> bool:
        return self._healthy


@pytest.mark.asyncio
async def test_router_uses_primary_when_healthy():
    primary = FakeProvider("gemini", "gemini-2.5-flash", True)
    fallback = FakeProvider("ollama", "qwen3:8b", True)

    router = ModelRouter(primary, fallback)

    response = await router.generate("Hello")

    assert response == "gemini: Hello"


@pytest.mark.asyncio
async def test_router_uses_fallback_when_primary_unhealthy():
    primary = FakeProvider("gemini", "gemini-2.5-flash", False)
    fallback = FakeProvider("ollama", "qwen3:8b", True)

    router = ModelRouter(primary, fallback)

    response = await router.generate("Hello")

    assert response == "ollama: Hello"


@pytest.mark.asyncio
async def test_router_streams_from_primary():
    primary = FakeProvider("gemini", "gemini-2.5-flash", True)
    fallback = FakeProvider("ollama", "qwen3:8b", True)

    router = ModelRouter(primary, fallback)

    chunks = []

    async for chunk in router.stream("Hello"):
        chunks.append(chunk)

    assert chunks == ["gemini: ", "Hello"]


@pytest.mark.asyncio
async def test_router_streams_from_fallback():
    primary = FakeProvider("gemini", "gemini-2.5-flash", False)
    fallback = FakeProvider("ollama", "qwen3:8b", True)

    router = ModelRouter(primary, fallback)

    chunks = []

    async for chunk in router.stream("Hello"):
        chunks.append(chunk)

    assert chunks == ["ollama: ", "Hello"]


@pytest.mark.asyncio
async def test_router_health_check_uses_primary_first():
    primary = FakeProvider("gemini", "gemini-2.5-flash", True)
    fallback = FakeProvider("ollama", "qwen3:8b", True)

    router = ModelRouter(primary, fallback)

    assert await router.health_check() is True


@pytest.mark.asyncio
async def test_router_health_check_falls_back():
    primary = FakeProvider("gemini", "gemini-2.5-flash", False)
    fallback = FakeProvider("ollama", "qwen3:8b", True)

    router = ModelRouter(primary, fallback)

    assert await router.health_check() is True