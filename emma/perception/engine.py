"""
EMMA Perception Engine.

Receives normalized InputEvent objects from different
input adapters and provides a unified perception interface.
"""

from __future__ import annotations

from emma.core.logger import get_logger
from emma.perception.shared.input_event import InputEvent
from emma.perception.input.text_input import TextInput

logger = get_logger(__name__)


class PerceptionEngine:
    """
    Central entry point for EMMA's perception system.

    Different input sources such as text, audio, vision,
    screen, and sensors eventually enter through this engine.
    """

    def __init__(self) -> None:
        self._running = False

    async def start(self) -> None:
        """Start the perception engine."""

        if self._running:
            return

        self._running = True
        logger.info("Perception Engine started.")

    async def stop(self) -> None:
        """Stop the perception engine."""

        if not self._running:
            return

        self._running = False
        logger.info("Perception Engine stopped.")

    async def process(self, event: InputEvent) -> InputEvent:
        """
        Process a normalized input event.

        For now, the engine simply validates and forwards
        the event. More advanced perception processing will
        be added later.
        """

        if not self._running:
            raise RuntimeError("Perception Engine is not running.")

        logger.info(
            "Processing input: source=%s",
            event.source.value,
        )

        return event

    async def process_text(self, text: str) -> InputEvent:
        """
        Convert text input into an InputEvent
        and process it through the perception engine.
        """

        text_input = TextInput()

        event = text_input.create_event(text)

        return await self.process(event)