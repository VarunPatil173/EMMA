"""
Asynchronous audio stream for EMMA perception.
"""

from __future__ import annotations

import asyncio

from emma.perception.audio.capture import AudioCapture
from emma.perception.audio.frame import AudioFrame


class AudioStream:
    """
    Continuously captures microphone frames and places them
    into an asynchronous queue.
    """

    def __init__(
        self,
        capture: AudioCapture,
        max_queue_size: int = 50,
    ) -> None:
        self.capture = capture
        self.queue: asyncio.Queue[AudioFrame] = asyncio.Queue(
            maxsize=max_queue_size
        )

        self._task: asyncio.Task[None] | None = None
        self._running = False

    async def start(self) -> None:
        """Start continuous audio capture."""

        if self._running:
            return

        self.capture.start()
        self._running = True

        self._task = asyncio.create_task(
            self._capture_loop()
        )

    async def _capture_loop(self) -> None:
        """Continuously capture audio frames."""

        while self._running:
            frame = await asyncio.to_thread(
                self.capture.read
            )

            if self.queue.full():
                # Drop the oldest frame to keep latency bounded.
                try:
                    self.queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass

            await self.queue.put(frame)

    async def read(self) -> AudioFrame:
        """Wait for and return the next available audio frame."""

        return await self.queue.get()

    async def stop(self) -> None:
        """Stop continuous audio capture."""

        if not self._running:
            return

        self._running = False

        if self._task is not None:
            await self._task
            self._task = None

        self.capture.stop()