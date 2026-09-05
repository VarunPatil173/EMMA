from collections.abc import AsyncIterator

from emma.intelligence.agent import Agent
from emma.intelligence.model import ModelProvider
from emma.intelligence.personality import emma_personality
from emma.intelligence.personality_prompt import build_personality_prompt
from emma.perception.shared.input_event import InputEvent


class GeneralAgent(Agent):
    def __init__(self, model: ModelProvider) -> None:
        self._model = model
        self._personality_prompt = build_personality_prompt(emma_personality)

    @property
    def name(self) -> str:
        return "general"

    async def run(self, event: InputEvent) -> str:
        text = event.text.strip()

        if not text:
            return "I didn't receive any text."

        return await self._model.generate(
            text,
            system_prompt=self._personality_prompt,
        )

    async def stream(self, event: InputEvent) -> AsyncIterator[str]:
        text = event.text.strip()

        if not text:
            yield "I didn't receive any text."
            return

        async for chunk in self._model.stream(
            text,
            system_prompt=self._personality_prompt,
        ):
            yield chunk