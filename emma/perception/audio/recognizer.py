"""
Speech recognition using Faster-Whisper.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from emma.core.logger import get_logger
from emma.perception.audio.speech_segment import SpeechSegment


logger = get_logger(__name__)


@dataclass(frozen=True)
class Transcript:
    """Result of speech recognition."""

    text: str


class WhisperRecognizer:
    """
    Converts SpeechSegment audio into text using Faster-Whisper.
    """

    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
        language: str | None = "en",
    ) -> None:

        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.language = language

        self._model = None

    def start(self) -> None:
        """Load the Whisper model."""

        from faster_whisper import WhisperModel

        logger.info(
            "Loading Faster-Whisper model: %s",
            self.model_size,
        )

        self._model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
        )

        logger.info("Faster-Whisper ready.")

    def transcribe(
        self,
        segment: SpeechSegment,
    ) -> Transcript:
        """
        Transcribe a speech segment.
        """

        if self._model is None:
            raise RuntimeError(
                "WhisperRecognizer must be started before transcription."
            )

        segments, _ = self._model.transcribe(
            segment.samples,
            language=self.language,
            vad_filter=False,
        )

        text = " ".join(
            part.text.strip()
            for part in segments
            if part.text.strip()
        ).strip()

        return Transcript(text=text)

    def stop(self) -> None:
        """Release the Whisper model."""

        self._model = None

        logger.info("Faster-Whisper stopped.")