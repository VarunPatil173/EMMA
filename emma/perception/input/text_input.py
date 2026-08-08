"""
EMMA Text Input Adapter.

Receives commands typed by the user and converts them
into EMMA InputEvent objects.
"""

from __future__ import annotations

from emma.core.logger import get_logger
from emma.perception.shared.input_event import InputEvent

logger = get_logger(__name__)


class TextInput:
    """
    Handles text commands entered by the user.
    """

    source = "text"

    def create_event(self, text: str) -> InputEvent:
        """
        Convert raw text into an InputEvent.
        """

        text = text.strip()

        if not text:
            raise ValueError("Text input cannot be empty.")

        event = InputEvent(
            source=self.source,
            text=text,
        )

        logger.info("Text input received.")

        return event