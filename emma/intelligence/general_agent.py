from collections.abc import AsyncIterator

from emma.intelligence.agent import Agent
from emma.intelligence.conversation import Conversation
from emma.intelligence.model import ModelProvider
from emma.intelligence.personality import emma_personality
from emma.intelligence.personality_prompt import build_personality_prompt
from emma.memory.memory_decision import MemoryDecision
from emma.memory.memory_manager import MemoryManager
from emma.perception.shared.input_event import InputEvent


class GeneralAgent(Agent):
    def __init__(
        self,
        model: ModelProvider,
        memory_manager: MemoryManager | None = None,
    ) -> None:
        self._model = model
        self._personality_prompt = build_personality_prompt(
            emma_personality
        )
        self._conversation = Conversation()
        self._memory_manager = memory_manager

    @property
    def name(self) -> str:
        return "general"

    def _build_memory_context(self, query: str) -> str | None:
        """Build context from EMMA's long-term memory."""

        if self._memory_manager is None:
            return None

        memories = self._memory_manager.retrieve(query)

        if not memories:
            return None

        lines = [
            "LONG-TERM MEMORY:",
            "The following facts were explicitly saved about the user:",
        ]

        for memory in memories:
            lines.append(f"- {memory.content}")

        return "\n".join(lines)

    def _build_system_prompt(self, query: str) -> str:
        """Build the complete system prompt."""

        prompt = self._personality_prompt

        memory_context = self._build_memory_context(query)

        if memory_context:
            prompt += "\n\n" + memory_context

        return prompt

    async def run(self, event: InputEvent) -> str:
        text = event.text.strip()

        if not text:
            return "I didn't receive any text."

        memory = MemoryDecision.extract_memory(text)

        if memory is not None:
            if self._memory_manager is not None:
                self._memory_manager.remember(memory)

            return "I'll remember that, sir."

        history = self._conversation.get_messages()

        response = await self._model.generate(
            text,
            system_prompt=self._build_system_prompt(text),
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

        memory = MemoryDecision.extract_memory(text)

        if memory is not None:
            if self._memory_manager is not None:
                self._memory_manager.remember(memory)

            yield "I'll remember that, sir."
            return

        history = self._conversation.get_messages()
        response_parts: list[str] = []

        async for chunk in self._model.stream(
            text,
            system_prompt=self._build_system_prompt(text),
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