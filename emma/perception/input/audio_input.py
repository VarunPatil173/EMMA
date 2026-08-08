"""
EMMA Audio Input Adapter.

Converts recognized speech into EMMA InputEvent objects.

Speech recognition itself will be connected later.
"""

from __future__ import annotations

from emma.core.logger import get_logger
from emma.perception.shared.input_event import InputEvent

logger = get_logger(__name__)


class AudioInput:
    """
    Handles text produced by the speech-recognition pipeline.
    """

    source = "audio"

    def create_event(self, transcript: str) -> InputEvent:
        """
        Convert a speech-recognition transcript into an InputEvent.
        """

        transcript = transcript.strip()

        if not transcript:
            raise ValueError("Voice transcript cannot be empty.")

        event = InputEvent(
            source=self.source,
            text=transcript,
        )

        logger.info("Voice input received.")

        return event