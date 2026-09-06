from collections.abc import AsyncIterator

from emma.intelligence.agent import Agent
from emma.intelligence.conversation import Conversation
from emma.intelligence.model import ModelProvider
from emma.intelligence.personality import emma_personality
from emma.intelligence.personality_prompt import build_personality_prompt
from emma.perception.shared.input_event import InputEvent


class GeneralAgent(Agent):
    def __init__(self, model: ModelProvider) -> None:
        self._model = model
        self._personality_prompt = build_personality_prompt(emma_personality)
        self._conversation = Conversation()

    @property
    def name(self) -> str:
        return "general"

    async def run(self, event: InputEvent) -> str:
        text = event.text.strip()

        if not text:
            return "I didn't receive any text."

        history = self._conversation.get_messages()

        response = await self._model.generate(
            text,
            system_prompt=self._personality_prompt,
            history=history,
        )

        self._conversation.add_user_message(text)
        self._conversation.add_assistant_message(response)

        return response

    async def stream(self, event: InputEvent) -> AsyncIterator[str]:
        text = event.text.strip()

        if not text:
            yield "I didn't receive any text."
            return

        history = self._conversation.get_messages()
        response_parts: list[str] = []

        async for chunk in self._model.stream(
            text,
            system_prompt=self._personality_prompt,
            history=history,
        ):
            response_parts.append(chunk)
            yield chunk

        response = "".join(response_parts)

        self._conversation.add_user_message(text)
        self._conversation.add_assistant_message(response)

    def clear_conversation(self) -> None:
        self._conversation.clear()

    def get_conversation(self):
        return self._conversation.get_messages()