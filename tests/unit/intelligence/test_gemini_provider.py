import pytest

from emma.intelligence.gemini_provider import GeminiProvider


@pytest.mark.asyncio
async def test_gemini_can_generate():
    provider = GeminiProvider()

    response = await provider.generate("Reply with exactly: EMMA ONLINE")

    assert response
    assert "EMMA" in response.upper()

@pytest.mark.asyncio
async def test_gemini_can_stream():
    provider = GeminiProvider()

    chunks = []

    async for chunk in provider.stream("Say hello to EMMA in one short sentence."):
        chunks.append(chunk)

    response = "".join(chunks)

    assert response
    