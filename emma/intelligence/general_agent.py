"""
General-purpose agent for EMMA.
"""

from __future__ import annotations

from emma.intelligence.agent import Agent
from emma.perception.shared.input_event import InputEvent


class GeneralAgent(Agent):
    """Basic general-purpose EMMA agent."""

    @property
    def name(self) -> str:
        return "general"

    async def run(self, event: InputEvent) -> str:
        """Process a user input event."""

        text = event.text.strip()

        if not text:
            return "I didn't receive any text."

        return f"You said: {text}"