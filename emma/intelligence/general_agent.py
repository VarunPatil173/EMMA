from emma.intelligence.agent import Agent
from emma.intelligence.model import ModelProvider
from emma.perception.shared.input_event import InputEvent


class GeneralAgent(Agent):
    def __init__(self, model: ModelProvider) -> None:
        self._model = model

    @property
    def name(self) -> str:
        return "general"

    async def run(self, event: InputEvent) -> str:
        text = event.text.strip()

        if not text:
            return "I didn't receive any text."

        return await self._model.generate(text)