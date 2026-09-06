from collections.abc import AsyncIterator

from emma.intelligence.conversation import Message
from emma.intelligence.model import ModelProvider


class ModelRouter(ModelProvider):
    """Routes requests between a primary and fallback model provider."""

    def __init__(
        self,
        primary: ModelProvider,
        fallback: ModelProvider,
    ) -> None:
        self._primary = primary
        self._fallback = fallback

    @property
    def name(self) -> str:
        return "router"

    @property
    def model(self) -> str:
        return self._primary.model

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        history: list[Message] | None = None,
    ) -> str:
        if await self._primary.health_check():
            return await self._primary.generate(
                prompt,
                system_prompt=system_prompt,
                history=history,
            )

        return await self._fallback.generate(
            prompt,
            system_prompt=system_prompt,
            history=history,
        )

    async def stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
        history: list[Message] | None = None,
    ) -> AsyncIterator[str]:
        if await self._primary.health_check():
            async for chunk in self._primary.stream(
                prompt,
                system_prompt=system_prompt,
                history=history,
            ):
                yield chunk

            return

        async for chunk in self._fallback.stream(
            prompt,
            system_prompt=system_prompt,
            history=history,
        ):
            yield chunk

    async def health_check(self) -> bool:
        primary_healthy = await self._primary.health_check()

        if primary_healthy:
            return True

        return await self._fallback.health_check()