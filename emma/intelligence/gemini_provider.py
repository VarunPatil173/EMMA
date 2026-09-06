from collections.abc import AsyncIterator

from google import genai
from google.genai import types

from emma.core.config import settings
from emma.intelligence.conversation import Message
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

    def _build_contents(
        self,
        prompt: str,
        history: list[Message] | None = None,
    ) -> list[types.Content]:
        contents: list[types.Content] = []

        if history:
            for message in history:
                role = "model" if message.role == "assistant" else "user"

                contents.append(
                    types.Content(
                        role=role,
                        parts=[
                            types.Part(
                                text=message.content,
                            )
                        ],
                    )
                )

        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        text=prompt,
                    )
                ],
            )
        )

        return contents

    def _build_config(
        self,
        system_prompt: str | None = None,
    ) -> types.GenerateContentConfig | None:
        if not system_prompt:
            return None

        return types.GenerateContentConfig(
            system_instruction=system_prompt,
        )

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        history: list[Message] | None = None,
    ) -> str:
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=self._build_contents(
                prompt=prompt,
                history=history,
            ),
            config=self._build_config(system_prompt),
        )

        return response.text or ""

    async def stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
        history: list[Message] | None = None,
    ) -> AsyncIterator[str]:
        response_stream = await self._client.aio.models.generate_content_stream(
            model=self._model,
            contents=self._build_contents(
                prompt=prompt,
                history=history,
            ),
            config=self._build_config(system_prompt),
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