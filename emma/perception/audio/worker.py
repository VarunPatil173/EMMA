"""
Continuous audio perception worker for EMMA.
"""

from __future__ import annotations

import asyncio

from emma.core.logger import get_logger
from emma.perception.audio.recognizer import WhisperRecognizer
from emma.perception.audio.segmenter import SpeechSegmenter
from emma.perception.audio.stream import AudioStream
from emma.perception.input.audio_input import AudioInput
from emma.perception.engine import PerceptionEngine


logger = get_logger(__name__)


class PerceptionWorker:
    """
    Connects the audio stream, speech segmentation,
    and speech recognition pipeline.
    """

    def __init__(
        self,
        stream: AudioStream,
        segmenter: SpeechSegmenter,
        recognizer: WhisperRecognizer,
        audio_input: AudioInput,
        engine: PerceptionEngine,
    ) -> None:
        self.stream = stream
        self.segmenter = segmenter
        self.recognizer = recognizer
        self.audio_input = audio_input
        self.engine = engine

        self._task: asyncio.Task[None] | None = None
        self._running = False

    async def start(self) -> None:
        """Start the perception pipeline."""

        if self._running:
            return

        self.recognizer.start()
        await self.stream.start()

        self._running = True

        self._task = asyncio.create_task(
            self._run(),
            name="emma-perception-worker",
        )

        logger.info("Perception worker started.")

    async def _run(self) -> None:
        """Continuously process incoming audio."""

        while self._running:

            frame = await self.stream.read()

            segment = self.segmenter.process(
                frame.samples
            )

            if segment is None:
                continue

            transcript = await asyncio.to_thread(
                self.recognizer.transcribe,
                segment,
            )

            if transcript.text:
                event = self.audio_input.create_event(
                    transcript.text
                )

                await self.engine.process(event)

    async def stop(self) -> None:
        """Stop the perception pipeline."""

        if not self._running:
            return

        self._running = False

        if self._task is not None:
            self._task.cancel()

            try:
                await self._task
            except asyncio.CancelledError:
                pass

            self._task = None

        await self.stream.stop()

        self.recognizer.stop()

        logger.info("Perception worker stopped.")