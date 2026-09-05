import pytest

from emma.intelligence.ollama_provider import OllamaProvider


@pytest.mark.asyncio
async def test_ollama_can_generate():
    provider = OllamaProvider("qwen3:8b")

    response = await provider.generate(
        "Reply with exactly: EMMA LOCAL ONLINE"
    )

    assert response
    assert "EMMA" in response.upper()


@pytest.mark.asyncio
async def test_ollama_can_stream():
    provider = OllamaProvider("qwen3:8b")

    chunks = []

    async for chunk in provider.stream(
        "Say hello to EMMA in one short sentence."
    ):
        chunks.append(chunk)

    response = "".join(chunks)

    assert response
    assert len(chunks) > 0


@pytest.mark.asyncio
async def test_ollama_health_check():
    provider = OllamaProvider("qwen3:8b")

    assert await provider.health_check()