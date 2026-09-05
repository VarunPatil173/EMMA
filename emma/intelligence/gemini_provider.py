from collections.abc import AsyncIterator

from google import genai

from emma.core.config import settings
from emma.intelligence.model import ModelProvider


class GeminiProvider(ModelProvider):
    def __init__(self) -> None:
        self._model = settings.llm.model
        self._client = genai.Client(api_key=settings.llm.api_key)

    @property
    def name(self) -> str:
        return "gemini"

    @property
    def model(self) -> str:
        return self._model

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        config = None

        if system_prompt:
            config = {
                "system_instruction": system_prompt,
            }

        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=config,
        )

        return response.text or ""

    async def stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> AsyncIterator[str]:
        config = None

        if system_prompt:
            config = {
                "system_instruction": system_prompt,
            }

        response_stream = await self._client.aio.models.generate_content_stream(
            model=self._model,
            contents=prompt,
            config=config,
        )

        async for chunk in response_stream:
            if chunk.text:
                yield chunk.text

    async def health_check(self) -> bool:
        try:
            response = await self._client.aio.models.generate_content(
                model=self._model,
                contents="Reply with OK.",
            )

            return bool(response.text)

        except Exception:
            return False