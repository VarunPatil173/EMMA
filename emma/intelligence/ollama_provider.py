from collections.abc import AsyncIterator

from ollama import AsyncClient

from emma.intelligence.model import ModelProvider


class OllamaProvider(ModelProvider):
    def __init__(self, model: str = "qwen3:8b") -> None:
        self._model = model
        self._client = AsyncClient()

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def model(self) -> str:
        return self._model

    async def generate(self, prompt: str) -> str:
        response = await self._client.chat(
            model=self._model,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        return response["message"]["content"]

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        response_stream = await self._client.chat(
            model=self._model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )

        async for chunk in response_stream:
            content = chunk["message"]["content"]

            if content:
                yield content

    async def health_check(self) -> bool:
        try:
            await self._client.chat(
                model=self._model,
                messages=[
                    {"role": "user", "content": "Reply with OK."},
                ],
            )
            return True
        except Exception:
            return False